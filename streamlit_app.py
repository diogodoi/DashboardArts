import streamlit as st
import pandas as pd
import numpy as np
from st_clickable_images import clickable_images
from database import data, data_imagens
from utils import compare_lists, change_images, find_clusters, create_rainbow, to_hex
import altair as alt

st.set_page_config(
    page_title="Diogo Godoi - Best Artworks of all times",
    page_icon=":spider_web:",
    layout="wide",

    initial_sidebar_state="expanded",
    menu_items={
        'About': "Dashboard desenvolvida para a disciplina de Vizualição de Dados."
    }
)

st.markdown('''
            <div style='display:grid;text-align:center;'>
            
            <h1>Best Artworks of all times</h1>            
                <p> by Diogo Godoi </p>                
            </div>
            
            ''',
            unsafe_allow_html=True)
genres = data.genre.explode().unique().tolist()


if 'art_key' not in st.session_state:
    st.session_state['art_key'] = -1

for name in data['name'].tolist():
    new_name = f'art_key_{name}'.replace(" ", "_")
    if new_name not in st.session_state:
        st.session_state[new_name] = -1


def change_path():
    if st.session_state['art_key'] != -1:
        path = change_images(
                imagens, path_list=st.session_state['paths'], art_key=st.session_state['art_key'], artists=None)
        return path
    else:
        for i in st.session_state:
            if 'art_key' in i:
                if st.session_state[i] != -1:
                    artists = i.replace("art_key_", "").replace("_", " ")
                    key = st.session_state[i]
                    path = change_images(
                        imagens, path_list=None, art_key=key, artists=artists)
                    return path


def change_state(name):
    path = imagens[imagens['name'] == name].path.to_list()
    st.session_state['paths'] = path


def on_genre_change():
    for i in st.session_state:
        if 'art_key' in i and st.session_state[i] != -1:
            st.session_state[i] = -1
        else:
            pass


def check_state_arts():
    values_state = [st.session_state[i]
                    for i in st.session_state if 'art_key' in i]
    for key in values_state:
        if key != -1:
            return True
    return False


select_genre = st.selectbox(
    "Selecione um gênero", options=genres, on_change=on_genre_change)


artistas_genero = data[data['genre'].map(
    lambda genre: select_genre in genre)]
names = artistas_genero['name'].to_list()
imagens = data_imagens[data_imagens['name'].map(
    lambda name: name in names)]
points = imagens['Rgb'].explode().to_list()
rgb_list = find_clusters(points, 12)
hex_list = to_hex(rgb_list)
st.session_state['genre_palete'] = hex_list
st.divider()
with st.container():

    col1, col2 = st.columns(2)

    if check_state_arts():
        with col1:
            st.session_state['paths'] = change_path()[:11]
            art_data = imagens[imagens['path'] == st.session_state['paths'][0]]
            create_rainbow(art_data=art_data)
            st.image(st.session_state['paths'][0], use_column_width=True)
    else:
        with col1:
            source = artistas_genero[['name', 'paintings']]
            total_data = source.paintings.sum()
            color = [alt.ColorValue(color)
                     for color in st.session_state['genre_palete']]
            hist_data = [{'Red': r, 'Green': g, 'Blue': b}
                         for r, g, b in imagens['Rgb'].explode()]
            hist_source = pd.DataFrame(hist_data)
            if source.name.__len__() > 1:
                st.subheader(f'Most common colors used in: {select_genre}')
                create_rainbow(pd.DataFrame(
                    {'Hex': [st.session_state['genre_palete']]}))
            st.subheader(
                f'Total works of art produced by {select_genre}')
            chart = (
                alt.Chart(source, width=560, height=420).mark_arc(innerRadius=140).encode(
                    theta="paintings",

                    color=alt.Color("name:N", scale=alt.Scale(
                        range=st.session_state['genre_palete'][:source.__len__()])).legend(None),
                )
            )
            text = (
                alt.Chart(pd.DataFrame({'Total_Artworks': [total_data]})).mark_text(size=24, align='center', baseline='middle', color="white").encode(
                    text='Total_Artworks:Q',

                )
            )
            donut_chart = chart+text
            st.altair_chart(donut_chart, use_container_width=True)
            hist = (
                alt.Chart(hist_source).transform_fold(['Red', 'Green', 'Blue'], as_=['var', 'val']).mark_bar(opacity=0.7, binSpacing=0).encode(
                    alt.X('val:Q', bin=alt.Bin(maxbins=255),
                          axis=alt.Axis(title='Tones')),
                    alt.Y('count()', stack=None),
                    color=alt.Color('var:N', scale=alt.Scale(
                        range=['blue', 'green', 'red']), legend=alt.Legend(title='Channels'))
                )
            )
            st.altair_chart(hist, use_container_width=True)
    with col2:
        if check_state_arts():
            art_data = imagens[imagens['path']
                               == st.session_state['paths'][0]]
            artist_data = data[art_data['name'].values[0] == data['name']]
            st.subheader(art_data['name'].values[0])
            st.divider()
            with st.expander('See more'):
                st.markdown(f'''
                                    {artist_data['nascimento'].values[0]}-{artist_data['morte'].values[0]}
                                    
                                    Nationality: { artist_data['nationality'].values[0]}
                                    
                                    Total of artworks: {artist_data['paintings'].values[0]}
                                                                
                                    {artist_data['bio'].values[0]}  
                                                            
                                    More info on: {artist_data['wikipedia'].values[0]}
                                ''')

            clicked = clickable_images(
                paths=st.session_state['paths'],
                div_style={"display": "flex",
                           "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "128px"},
                key='art_key'
            )

        else:
            for n, i in enumerate(artistas_genero.sort_values(by='name').iterrows()):
                points = imagens[i[1]['name'] ==
                                 imagens['name']].Rgb.explode().to_list()
                rgb_list = find_clusters(points, 12)
                hex_list = to_hex(rgb_list)
                st.markdown(
                    f'<h2 style="color:{st.session_state["genre_palete"][n]}; cursor:pointer;">{i[1]["name"]}</h2>', unsafe_allow_html=True)
                st.text('Most common colors used:')
                create_rainbow(pd.DataFrame({'Hex': [hex_list]}))
                expander = st.expander('See more')
                with expander:
                    st.markdown(f'''
                                    {i[1]['nascimento']}-{i[1]['morte']}
                                    
                                    Nationality: {[i for i in i[1]['nationality']]}
                                    
                                    Total of artworks: {i[1]['paintings']}
                                                                
                                    {i[1]['bio']}  
                                                            
                                    More info on: {i[1]['wikipedia']}
                                ''')
                    st.divider()
                    change_state(i[1]['name'])
                    clickable_images(
                        st.session_state['paths'],
                        div_style={"display": "flex",
                                   "flex-wrap": "wrap"},
                        img_style={"margin": "5px", "height": "64px"},
                        key=f'art_key_{i[1]["name"].replace(" ","_")}'
                    )

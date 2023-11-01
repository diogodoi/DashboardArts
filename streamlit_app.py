import streamlit as st
import pandas as pd
from st_clickable_images import clickable_images
from database import data, data_imagens
from utils import change_images, find_clusters, create_rainbow, to_hex, hex_to_rgb, compare_lists
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
    st.session_state['top_art_paths'] = -1

for name in data['name'].tolist():
    new_name = f'art_key_{name}'.replace(" ", "_")
    if new_name not in st.session_state:
        st.session_state[new_name] = -1


def change_path():
    if st.session_state['art_key'] != -1:
        path = change_images(
            imagens, path_list=st.session_state['paths'], art_key=st.session_state['art_key'], artists=None)
        return path
    if st.session_state['top_art_paths'] != -1:
        path = change_images(
            data_imagens, path_list=st.session_state['paths'], art_key=st.session_state['top_art_paths'], artists=None)
        return path
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
    st.session_state['top_art_paths'] = -1
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


def check_all_arts():
    if st.session_state['top_art_paths'] != -1:
        return True
    return False

def find_arts_by_color(color):
    try:
        to_rgb = hex_to_rgb(color[1:])
        list_images_points = data_imagens['central_point'].values
        closes_index = compare_lists(to_rgb, list_images_points)[:20]
        st.session_state['paths'] = data_imagens.iloc[closes_index].path.values.tolist(
        )
        print(st.session_state['paths'])
    except:
        print('erro')


def create_image_full(data):
    st.session_state['paths'] = change_path()[:11]
    art_data = data[data['path']
                    == st.session_state['paths'][0]]
    create_rainbow(art_data=art_data)
    st.image(st.session_state['paths'][0], use_column_width=True)


def create_art_info(data_imagens, all: bool = False):
    art_data = data_imagens[data_imagens['path']
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
    if all:
        point = art_data['central_point'].values[0]
        points_list = data_imagens['central_point'].values
        closest = compare_lists(point, points_list)[:20]
        path = [data_imagens['path'].iloc[index]for index in closest]
        st.session_state['paths'] = path
        key = 'top_art_paths'
    else:
        key = 'art_key'

    clickable_images(
        paths=st.session_state['paths'],
        div_style={"display": "flex",
                   "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "128px"},
        key=key
    )


with st.sidebar:
    select_genre = st.selectbox(
        "Select genre:", options=genres, on_change=on_genre_change)
    color_selected = st.color_picker(
        'Select color:', '#000')
    color_button = st.button(
        'Find now!', key='color_button', use_container_width=True)
    if color_button:
        find_arts_by_color(color_selected)
    else:
        pass


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
    if color_button:
            st.markdown(f'''
                        <h1 style="text-align:center>Color select: {color_selected} </h1>
                        ''', unsafe_allow_html=True)

            clickable_images(
                paths=st.session_state['paths'],
                div_style={"display": "flex",
                           "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "256px"},
                key='top_art_paths'
            )
            color_button = False
    else:
        if check_all_arts():
            with col1:
                create_image_full(data_imagens)
            with col2:
                create_art_info(data_imagens, all=True)
        else:
            if check_state_arts():
                with col1:
                    create_image_full(imagens)
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
                        st.subheader(
                            f'Most common colors used in: {select_genre}')
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
                    create_art_info(imagens)
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

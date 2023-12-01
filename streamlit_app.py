import streamlit as st
import pandas as pd
from st_clickable_images import clickable_images
from database import *
from utils import *
import altair as alt
from plotly.express import scatter_3d, scatter
from sklearn.cluster import KMeans

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
genres = ['Select Genre']
for i in data.genre.explode().unique().tolist():
    genres.append(i)


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
    to_rgb = hex_to_rgb(color[1:])
    list_images_points = data_imagens['central_point'].values
    closes_index = compare_lists(to_rgb, list_images_points)[:20]
    paths = data_imagens.iloc[closes_index].path.values.tolist(
    )
    return paths


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
        st.subheader("Top 20 images that have the same pallete of colors.")
    else:
        key = 'art_key'
        st.subheader(
            f"Top 10 images from {select_genre} that have the same pallete of colors.")

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
        label='Find one artwork that have this color:', args='#000',)
    color_button = st.button(
        'Find now!', key='color_button', use_container_width=True)
    if color_button:
        find_arts_by_color(color_selected)
        st.session_state['top_art_paths'] = -2


st.divider()
if ((select_genre == 'Select Genre') and (st.session_state['top_art_paths'] == -1)):
    st.markdown(
        f'''<divs tyle = "text-align:center;">
            <h1 > Select a genre or pick a color in the sidebar to explore the colors of the genres.</h1>
            <h2> Or you can explore some information about artirts who participated from 2 diferents genres. </h2>
            ''', unsafe_allow_html=True)
    
    menu_data = data[data['size_genre'] == 'B'][['name', 'genre']]
    databases_options = ['PCA', 'TSNE', 'TSNE_auto_computed']

    databases_coords_caracteristicas = {
        'PCA': PCA_COORDS_HSV,
        'TSNE': TSNE_COORDS_HSV,
        'TSNE_auto_computed': TSNE_COORDS_auto_computed_HSV}

    databases_coords_cores = {
        'PCA': PCA_COORDS_COLORS,
        'TSNE': TSNE_COORDS_COLORS,
        'TSNE_auto_computed': TSNE_COORDS_auto_computed_COLORS
    }

    menu_col1,menu_col2,menu_col3 = st.columns(3)

    with menu_col1:
        name_selected = st.selectbox(
            'Select Artist', options=menu_data['name'].values)
    with menu_col2:
        genre_of_artists = menu_data[menu_data['name']
                                    == name_selected]['genre'].explode()
        genre_selected = st.selectbox('Select Genre', options=genre_of_artists)
    with menu_col3:
        select_coords = st.selectbox(
            'Select Coordinates', options=databases_options)


    coordenadas_caracteristicas = get_coordenadas(
        name_selected, genre_selected, databases_coords_caracteristicas[select_coords])
    labels_caracteristicas = coordenadas_caracteristicas['class'].map(lambda x: 'Art from ' + genre_selected if x == 'A' else 'Art from '+ name_selected)
    coordenadas_cores = get_coordenadas(
        name_selected, genre_selected, databases_coords_cores[select_coords])
    labels_cores = coordenadas_cores['class'].map(lambda x: 'Art from ' + genre_selected if x == 'A' else 'Art from '+ name_selected)



    col_coords_1, col_coords_2 = st.columns(2)
    with col_coords_1:
        st.title('CARACTERISTICS COORDINATES')
        fig_caracteristicas = scatter_3d(coordenadas_caracteristicas, x=coordenadas_caracteristicas['x'], y=coordenadas_caracteristicas[
                                        'y'], z=coordenadas_caracteristicas['z'], color=labels_caracteristicas)
        st.plotly_chart(fig_caracteristicas)
    with col_coords_2:
        st.title('COLORS COORDINATES')
        fig_cores = scatter_3d(
            coordenadas_cores, x=coordenadas_cores['x'], y=coordenadas_cores['y'], z=coordenadas_cores['z'], color=labels_cores)
        st.plotly_chart(fig_cores)

    try:
        dists_caracteristicas = get_distances(coordenadas_caracteristicas)
        dists_cores = get_distances(coordenadas_cores)
    except:
        pass

    try:
        st.title('Relationship between means of distance from coordinates')
        dists_caracteristicas_imgs_index = dists_caracteristicas['imgs_index']
        dists_caracteristicas = dists_caracteristicas.drop(
            columns=['index', 'imgs_index'])
        dists_mean_caracteristicas = dists_caracteristicas.T.mean()
        dists_cores_imgs_index = dists_cores['imgs_index']
        dists_cores = dists_cores.drop(columns=['index', 'imgs_index'])
        dists_mean_cores = dists_cores.T.mean()
        df_dists = pd.DataFrame(
            {
                'x': dists_mean_caracteristicas,
                'y': dists_mean_cores
            }
        )
        labels = KMeans(n_clusters=2).fit_predict(df_dists.to_numpy())
        df_dists['imgs_index'] = dists_cores_imgs_index
        df_dists['labels'] = labels
        df_dists['labels'] = df_dists['labels'].map(lambda x: 'A' if x == 0 else 'B' )
        fig_dists = scatter(df_dists, x='y', y='x',
                            color='labels', hover_data='imgs_index',labels={'x':'Mean of distance from caracteristics','y':'Mean of distance from colors'})
        st.plotly_chart(fig_dists, use_container_width=True)
        col_imgs_0, col_imgs_1 = st.columns(2)
        with col_imgs_0:
            st.title('A')
            index_0 = df_dists[df_dists['labels']=='A']['imgs_index'].values
            
            clickable_images(
                paths=data_imagens.iloc[index_0]['path'].to_list(),
                titles=df_dists[df_dists['labels']=='A']['imgs_index'].to_list(),            
                div_style={"display": "flex",
                        "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "128px"},
            )
        with col_imgs_1:
            st.title('B')
            index_1 = df_dists[df_dists['labels']=='B']['imgs_index'].values
            clickable_images(
                paths=data_imagens.iloc[index_1]['path'].to_list(),
                titles= df_dists[df_dists['labels']=='B']['imgs_index'].to_list(),
                div_style={"display": "flex",
                        "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "128px"},
            )


    except:
        st.title('There is no artists to compare !')

else:
    with st.container():
        col1, col2 = st.columns(2)
        if color_button:
            st.markdown(f'''
                            <h1 style="text-align:center;">The 20 artworks that have the color: <div style="background-color:{color_selected};">{color_selected}</div></h1>
                            ''', unsafe_allow_html=True)

            clickable_images(
                paths=st.session_state['paths'],
                div_style={"display": "flex",
                           "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "256px"},
                key='top_art_paths'
            )
        else:
            if check_all_arts():
                with col1:
                    create_image_full(data_imagens)
                with col2:
                    create_art_info(data_imagens, all=True)
            else:
                artistas_genero = data[data['genre'].map(
                    lambda genre: select_genre in genre)]
                names = artistas_genero['name'].to_list()
                imagens = data_imagens[data_imagens['name'].map(
                    lambda name: name in names)]
                points = imagens['Rgb'].explode().to_list()
                rgb_list = find_clusters(points, 12)
                hex_list = to_hex(rgb_list)
                st.session_state['genre_palete'] = hex_list
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
                                    img_style={"margin": "5px",
                                               "height": "64px"},
                                    key=f'art_key_{i[1]["name"].replace(" ","_")}'
                                )

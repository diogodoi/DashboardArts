import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from streamlit import markdown
import altair as alt
import streamlit as st
from matplotlib import patches
from database import *

def plota_cores(points):
    fig, ax = plt.subplots(figsize=(20, 4))

    for i, cor in enumerate(points):
        ax.bar(i, 1, color=cor)

    # Configure os rótulos do eixo X
    plt.xticks(np.arange(len(points)), points, rotation=90)
    ax.set_xlabel('Cores Hexadecimais')

    # Inverter o eixo Y
    ax.invert_yaxis()

    # Ocultar os eixos
    ax.axis('off')
    return fig


def hex_to_rgb(hex):
    return list(int(hex[i:i+2], 16) for i in (0, 2, 4))


def to_hex(lista_rgb):
    return sorted(['#{:02x}{:02x}{:02x}'.format(*cor) for cor in lista_rgb], reverse=True)


def find_clusters(points, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    kmeans.fit(points)
    points = kmeans.cluster_centers_.astype(int)
    return points


def compare_lists(point, points_list):
    n = points_list.shape[0]
    distances = []
    for i in range(n):
        dist = np.linalg.norm(point - points_list[i])
        distances.append(dist)
    nearest_indices = np.argsort(distances)
    return nearest_indices


def change_images(imagens, path_list: None, art_key, artists: None):
    if artists != None:
        path_artists = imagens[imagens['name'] == artists].path.to_list()[
            art_key]
        point = imagens[imagens['path'] ==
                        path_artists].central_point.values[0]
    else:
        point = imagens[imagens['path'] ==
                        path_list[art_key]].central_point.values[0]
    lista_artes = compare_lists(point, imagens['central_point'].values)
    new_path = [imagens['path'].iloc[index] for index in lista_artes]
    return new_path


def create_rainbow(art_data):
    markdown(f''' 
                                <div style='display:flex;flex-direction:row;margin-bottom:12px; flex-wrap:wrap;'>
                                <div style='background-color:{art_data.Hex.values[0][0]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][0]}</div>                                
                                <div style='background-color:{art_data.Hex.values[0][1]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][1]}</div>
                                <div style='background-color:{art_data.Hex.values[0][2]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][2]}</div>
                                <div style='background-color:{art_data.Hex.values[0][3]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][3]}</div>
                                <div style='background-color:{art_data.Hex.values[0][4]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][4]}</div>
                                <div style='background-color:{art_data.Hex.values[0][5]}; width:64px;height:32px;align-items:center;justify-items:center;color:#000'>{art_data.Hex.values[0][5]}</div>
                                <div style='background-color:{art_data.Hex.values[0][6]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][6]}</div>
                                <div style='background-color:{art_data.Hex.values[0][7]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][7]}</div>
                                <div style='background-color:{art_data.Hex.values[0][8]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][8]}</div>
                                <div style='background-color:{art_data.Hex.values[0][9]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][9]}</div>
                                <div style='background-color:{art_data.Hex.values[0][10]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][10]}</div>
                                <div style='background-color:{art_data.Hex.values[0][11]}; width:64px;height:32px;align-items:center;justify-items:center;color:#fff'>{art_data.Hex.values[0][11]}</div>
                                </div>
                            ''', unsafe_allow_html=True)


def get_coordenadas(artist_name,genre,array_coordenadas):
    artists_name_list_to_compare = data[data['genre'].map(lambda x: x.__len__() ==1 and genre in x)]['name'].values.tolist()
    
    df_artista_genero = pd.DataFrame(array_coordenadas[data_imagens[data_imagens['name'].map(lambda x: x in artists_name_list_to_compare)].index])
    df_artista_genero=df_artista_genero.rename(columns={0:'x',1:'y',2:'z'})
    df_artista_genero['index_imgs'] = data_imagens[data_imagens['name'].map(lambda x: x in artists_name_list_to_compare)].index
    df_artista_genero['class'] = 'A'
    
    df_artista_busca = pd.DataFrame(array_coordenadas[data_imagens[data_imagens['name']== artist_name].index])
    df_artista_busca = df_artista_busca.rename(columns={0:'x',1:'y',2:'z'})
    df_artista_busca['index_imgs'] = data_imagens[data_imagens['name']== artist_name].index
    df_artista_busca['class'] = 'B'
    
    frames = [df_artista_genero,df_artista_busca]
    coordenadas = pd.concat(frames)
    
    return coordenadas

def get_distances(coordenadas):
    len_artists = coordenadas[coordenadas['class']=='A'].__len__()
    dists = pd.DataFrame(pairwise_distances(coordenadas[['x','y','z']]))

    dists = dists.iloc[len_artists:,:len_artists].rename(columns=coordenadas['index_imgs'][:len_artists])
    dists['imgs_index'] = coordenadas['index_imgs'][len_artists:].values
    dists = dists.reset_index()
    return dists
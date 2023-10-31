import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from streamlit import markdown



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


def to_hex(lista_rgb):
    return sorted(['#{:02x}{:02x}{:02x}'.format(*cor) for cor in lista_rgb],reverse=True)


def find_clusters(points,n_clusters):
    kmeans = KMeans(n_clusters=n_clusters,n_init='auto')
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

def change_images(imagens,path_list:None,art_key ,artists:None):
    if artists != None:
        path_artists = imagens[imagens['name']== artists].path.to_list()[art_key]
        point = imagens[imagens['path'] == path_artists].central_point.values[0]
    else:
        point = imagens[imagens['path'] == path_list[art_key]].central_point.values[0]
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


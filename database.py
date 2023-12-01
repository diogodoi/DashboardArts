import pandas as pd
import numpy as np


data = pd.read_csv('./artists.csv')
data['years'] = data['years'].apply(
    lambda x: x.replace('-', '–').strip().split('–'))
data['nascimento'] = data['years'].apply(
    lambda x: x[0].strip()).astype(np.int32)
data['morte'] = data['years'].apply(lambda x: x[1].strip()).astype(np.int32)
data['idade'] = data['morte'] - data['nascimento']
data = data.drop(columns=['years', 'id'])
data['genre'] = data['genre'].str.split(',')
data['nationality'] = data['nationality'].str.split(',')
genres = data.genre.explode().unique().tolist()
nationalitys = data.nationality.explode().unique()

def verify_num_genre(genre):
    len_gen = genre.__len__()
    if len_gen > 1:
        return 'B'
    else:
        return 'A'
#Nova coluna que verifica se o artista participou de mais de um gênero.
data['size_genre'] = data['genre'].map(lambda genre: verify_num_genre(genre))

data_imagens = pd.read_csv('./data_cores.csv', index_col=0, sep=';')
data_imagens['Rgb'] = data_imagens['Rgb'].map(lambda x: eval(x))
data_imagens['Hex'] = data_imagens['Hex'].map(lambda x: eval(x))
data_imagens['central_point'] = data_imagens['central_point'].map(
    lambda x: np.array(eval(x)))


genres = data['genre'].explode().unique().tolist()


## COORDENADAS

PCA_COORDS_HSV = pd.read_csv('./PCA_COORDS_HSV.csv',index_col=0)
PCA_COORDS_HSV = np.array(PCA_COORDS_HSV)
TSNE_COORDS_HSV = pd.read_csv('./TSNE_COORDS_HSV.csv',index_col=0)
TSNE_COORDS_HSV = np.array(TSNE_COORDS_HSV)
TSNE_COORDS_auto_computed_HSV = pd.read_csv('./TSNE_COORDS_auto_computed_HSV.csv',index_col=0)
TSNE_COORDS_auto_computed_HSV = np.array(TSNE_COORDS_auto_computed_HSV)

PCA_COORDS_COLORS = pd.read_csv('./PCA_COORDS_COLORS.csv',index_col=0)
PCA_COORDS_COLORS = np.array(PCA_COORDS_COLORS)
TSNE_COORDS_COLORS = pd.read_csv('./TSNE_COORDS_COLORS.csv',index_col=0)
TSNE_COORDS_COLORS = np.array(TSNE_COORDS_COLORS)
TSNE_COORDS_auto_computed_COLORS = pd.read_csv('./TSNE_COORDS_auto_computed_COLORS.csv',index_col=0)
TSNE_COORDS_auto_computed_COLORS = np.array(TSNE_COORDS_auto_computed_COLORS)
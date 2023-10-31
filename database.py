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

data_imagens = pd.read_csv('./data_cores.csv', index_col=0, sep=';')
data_imagens['Rgb'] = data_imagens['Rgb'].map(lambda x: eval(x))
data_imagens['Hex'] = data_imagens['Hex'].map(lambda x: eval(x))
data_imagens['central_point'] = data_imagens['central_point'].map(
    lambda x: np.array(eval(x)))

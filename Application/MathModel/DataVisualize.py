import joblib
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from Utils import get_color, draw_scatter

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')


# Normalize
def get_normalize(data):
    prepress = Normalizer()
    X = prepress.fit_transform(data)
    return X


# t-SNE
def t_SNE(data, dim=2, perp=30, with_normalize=False):
    if with_normalize:
        data = get_normalize(data)

    data = np.array(data)
    tsne = TSNE(n_components=dim, init='pca', perplexity=perp, method='exact')
    tsne.fit_transform(data)

    return tsne.embedding_


# PCA
def get_pca(data, c=3, with_normalize=False):
    if with_normalize:
        data = get_normalize(data)

    pca_result = PCA(n_components=c)
    pca_result.fit(data)
    newX = pca_result.fit_transform(data)

    return newX, pca_result.explained_variance_ratio_, pca_result


colors = get_color(rate, colors=None)

# t-SNE
dim_data = t_SNE(data_after_process, perp=50, with_normalize=True)

# # PCA
# dim_data, ratio, result = get_pca(data_after_process, c=2, with_normalize=False)
# print(ratio)

joblib.dump(dim_data, 'data/dim_data.pkl')

# get two coordinates
x = [i[0] for i in dim_data]
y = [i[1] for i in dim_data]

draw_scatter(x, y, rate, colors)

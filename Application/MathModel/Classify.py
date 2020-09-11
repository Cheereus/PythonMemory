import numpy as np
import joblib
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.neighbors import KNeighborsClassifier
from Utils import get_color, draw_scatter
from Metrics import ARI, accuracy, NMI, F1

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_after_process.pkl')

def knn(X, y, k):
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X, y)
    return knn_model

model = knn(data_after_process, rate, 3)

labels_predict = model.predict(data_after_process)

print('Accuracy:', accuracy(labels_predict, rate))

# get color list based on labels
default_colors = ['c', 'b', 'g', 'r', 'm', 'y', 'k']
colors = get_color(labels_predict, default_colors)

# draw
print('ARI:', ARI(rate, labels_predict))
print('NMI:', NMI(rate, labels_predict))
print('F1:', F1(rate, labels_predict))

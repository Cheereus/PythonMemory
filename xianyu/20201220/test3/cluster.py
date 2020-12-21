import numpy as np
from sklearn import metrics
# 使用k_mean进行聚类
from sklearn.cluster import KMeans, DBSCAN
from collections import Counter
import matplotlib.pyplot as plt


default_colors = ['c', 'g', 'r', 'b', 'k']
data = np.load('Data_for_Cluster.npz')
X = data['X']
label_true = data['labels_true']


# 根据类别获取颜色
def get_color(labels, colors=None):
    len_labels = len(labels)
    t = 0
    c = [None] * len_labels
    count_result = Counter(labels)
    colors = colors or default_colors
    # colors = colors or range(1, len(count_result.keys()) + 1)

    for i in count_result.keys():
        for j in range(len_labels):
            if i == labels[j]:
                c[j] = colors[t]
        t += 1

    return c


# 根据类别及颜色画出散点图
def draw_scatter(x, y, labels, colors, title):
    len_labels = len(labels)
    t = 0
    count_result = Counter(labels)
    plt.figure(figsize=(15, 15))

    for i in count_result.keys():
        xi = []
        yi = []
        ci = []
        for j in range(len_labels):
            if i == labels[j]:
                xi.append(x[j])
                yi.append(y[j])
                ci.append(colors[j])
        plt.scatter(xi, yi, c=ci, label=i, s=10)
        t += 1

    plt.legend(loc='best')
    plt.title(title)
    plt.show()


# k-means 聚类及绘图
km2 = KMeans(n_clusters=3).fit(X)
print(km2.labels_)
color = get_color(km2.labels_)
draw_scatter(X[:, 0], X[:, 1], km2.labels_, color, title='K-means')

# DBSCAN 聚类及绘图
DB_cluster = DBSCAN(eps=0.4, min_samples=5).fit(X)
print(DB_cluster.labels_)
color = get_color(DB_cluster.labels_)
draw_scatter(X[:, 0], X[:, 1], DB_cluster.labels_, color, title='DBSCAN')

# 输出两种方法的轮廓系数
print("轮廓系数：", metrics.silhouette_score(X, km2.labels_, metric='euclidean'))
print("轮廓系数：", metrics.silhouette_score(X, DB_cluster.labels_, metric='euclidean'))

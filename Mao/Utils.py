"""
Description:
Author: CheeReus_11
Date: 2020-08-08 17:42:59
LastEditTime: 2020-08-10 16:38:59
LastEditors: CheeReus_11
"""

from collections import Counter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

default_colors = ['c', 'b', 'g', 'r', 'm', 'y', 'k']
# default_colors = [[1, 0, 0],[0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1], [0.5, 0.5, 0.5]]
# default_colors = [[0, 0.8, 1], [0, 0.5, 0.5], [0.2, 0.8, 0.8], [0.2, 0.4, 1], [0.6, 0.8, 1], [1, 0.6, 0.8],
#                   [0.8, 0.6, 1], [1, 0.8, 0.6]]


# Get color list for drawing based on labels, more color values can also be customized
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


# draw with label TODO include the get_color function to simplify
def draw_scatter(x, y, labels, colors, title='pca', xlabel='x', ylabel='y'):
    len_labels = len(labels)
    t = 0
    count_result = Counter(labels)
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    fig = plt.figure(figsize=(15, 15))
    plt.xlim(-0.015, 0.025)
    plt.ylim(-0.025, 0.025)

    ax = plt.gca()
    # 设置图例字体大小
    ax.legend(fontsize=20)
    # ax.set_aspect('1', adjustable='box')
    # plt.xticks([])
    # plt.yticks([])
    # ax.axes.xaxis.set_ticklabels([])
    # ax.axes.yaxis.set_ticklabels([])
    # ax.axes.xaxis.set_ticks([])
    # ax.axes.yaxis.set_ticks([])
    for i in count_result.keys():
        xi = []
        yi = []
        ci = []
        for j in range(len_labels):
            if i == labels[j]:
                xi.append(x[j])
                yi.append(y[j])
                ci.append(colors[j])
        plt.scatter(xi, yi, c=ci, label=i, s=60, alpha=0.6)
        t += 1

    # if title:
    #     plt.title(title)
    plt.legend(loc='best', fontsize=15)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.grid(alpha=0.3)
    plt.show()

    # 文章中需要用到矢量图
    fig.savefig('images/' + title + '.svg', dpi=600, format='svg', bbox_inches='tight')
    # 普通图片
    fig.savefig('images/' + title + '.png')


# draw with label TODO include the get_color function to simplify
def draw_scatter3d(x, y, z, labels, colors):

    fig = plt.figure()
    ax = Axes3D(fig)

    len_labels = len(labels)
    t = 0
    count_result = Counter(labels)

    for i in count_result.keys():
        xi = []
        yi = []
        zi = []
        ci = []
        for j in range(len_labels):
            if i == labels[j]:
                xi.append(x[j])
                yi.append(y[j])
                zi.append(z[j])
                ci.append(colors[j])
        ax.scatter3D(xi, yi, zi, c=ci, label=i)
        t += 1

    plt.legend(loc='best')
    plt.show()


# Read data from `.txt` file
def read_from_txt(filePath, head=True):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(str, line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    # 去表头
    if head:
        data_list = data_list[1:]
    else:
        pass
    array_data = np.array(data_list)
    return array_data

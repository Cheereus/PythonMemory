from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from collections import Counter
import matplotlib.pyplot as plt

default_colors = ['c', 'r']


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


X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=0)  # 100个点 2类 2标签
# x为数据集的feature，y为label.
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 绘图
color = get_color(y)
draw_scatter(X[:, 0], X[:, 1], y, color, title='data-points')

# 标准化
standardScaler = StandardScaler()
standardScaler.fit(x_train)
X_standard = standardScaler.transform(x_train)

# 硬间隔支持向量机
svc = LinearSVC(C=10**4)
svc.fit(X_standard, y_train)
y_pred = svc.predict(standardScaler.transform(x_test))

# 计算准确率
print('C=10^4时准确率', accuracy_score(y_pred, y_test))

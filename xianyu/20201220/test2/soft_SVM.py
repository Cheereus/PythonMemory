import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, precision_score
from matplotlib.colors import ListedColormap

# 数据集读取及划分
iris = datasets.load_iris()
X_train = iris.data[:130]
y_train = iris.target[:130]
X_train = X_train[:, :2]
X_test = iris.data[130:]
y_test = iris.target[130:]
X_test = X_test[:, :2]

# 标准化
standardScaler = StandardScaler()
standardScaler.fit(X_train)
X_standard = standardScaler.transform(X_train)

# 使用 rbf 核的软间隔支持向量机
soft_svm = SVC(kernel='rbf')
soft_svm.fit(X_standard, y_train)
y_pred = soft_svm.predict(standardScaler.transform(X_test))

# 计算准确率、召回率、精准率
acc = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred, average='weighted')
precision = precision_score(y_test, y_pred, average='weighted')
print('acc', 'recall', 'precision')
print(acc, recall, precision)


# 绘制支持向量机的决策边界
def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    # 定义颜色和标记符号，通过颜色列图表生成颜色示例图
    marker = ('o', 'x', 's', 'v', '^')
    colors = ('lightgreen', 'blue', 'red', 'cyan', 'gray')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # 可视化决策边界
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # 绘制所有的样本点
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8,
                    c=cmap(idx), marker=marker[idx], s=73, label=cl)

    # 使用小圆圈高亮显示测试集的样本
    if test_idx:
        X_test, y_test = X[test_idx, :], y[test_idx]
        plt.scatter(X_test[:, 0], X_test[:, 1], c='', alpha=1.0, linewidth=1,
                    edgecolors='black', marker='o', s=135, label='test set')


X_combined_std = np.vstack((X_standard, standardScaler.transform(X_test)))
y_combined = np.hstack((y_train, y_test))

plt.figure(figsize=(12, 7))
plot_decision_regions(X_combined_std, y_combined, classifier=soft_svm,
                      test_idx=range(105, 150))
plt.legend(loc=2, fontsize=15, scatterpoints=2)
plt.show()

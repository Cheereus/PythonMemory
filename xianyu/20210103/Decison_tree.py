import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pydotplus
import graphviz
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 读取数据及标签
data = pd.read_csv('heart_disease5597/data.csv').values
y = data[:, -1]

# tSNE 降维
x_embed = TSNE(n_components=2).fit_transform(data)

# 绘制散点图
colors = ['red', 'black']
labels = ['sick', 'healthy']
for i in range(x_embed.shape[1]):
    plt.scatter(x_embed[y == i, 0], x_embed[y == i, 1], c = colors[i], label = labels[i])
plt.legend()
plt.show()

# 数据集划分
x_train, x_test, y_train, y_test = train_test_split(x_embed, y, test_size=0.2, random_state=0)

# 决策树训练及预测
clf = DecisionTreeClassifier(random_state=0, max_depth=8).fit(x_train, y_train)
y_pred = clf.predict(x_test)

# 输出准确率
print(accuracy_score(y_pred, y_test))

# 绘制决策树并保存为 pdf 文件
dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=['AT1', 'AT2'],
                                class_names=['sick', 'healthy'],
                                filled=True, rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("result1.pdf")







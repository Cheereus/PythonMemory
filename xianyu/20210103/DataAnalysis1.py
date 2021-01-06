import pandas as pd
from sklearn.feature_selection import f_classif
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# 读取数据及标签
data = pd.read_csv('heart_disease5597/data.csv', header=None).values
print(data.shape)
y = data[:, -1]
data = data[:, :-1]

y_label = ['年龄', '性别', '胸痛类型', '静息血压',
           '血浆类固醇含量', '空腹血糖', '静息心电图结果',
           '最高心率', '运动型心绞痛', '运动引起的ST下降',
           '最大运动量时心电图ST的斜率', '使用荧光染色法测定的主血管数',
           'THAL', '患病情况']

# 绘制散点图
colors = ['black', 'red']
labels = ['健康', '患病']
for i in range(2):
    plt.scatter(data[y == i + 1, 0], data[y == i + 1, 12], c=colors[i], label=labels[i])

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文显示
plt.rcParams["axes.unicode_minus"] = False  # 支持负号显示
plt.xlabel('年龄')
plt.ylabel('THAL')
plt.legend()
plt.show()

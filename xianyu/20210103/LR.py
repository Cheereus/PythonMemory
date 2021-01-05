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

# 使用方差分析（ANOVA）对各个特征计算p值
f, p = f_classif(data, y)

idx = np.argsort(-p)
print(p)
# print(f, f.shape, '\n', p, p.shape, '\n', idx, '\n', p[idx])
print(idx+1)
print(np.array(y_label)[idx])
acc = []

for i in range(0, 10):
    x_train, x_test, y_train, y_test = train_test_split(data[:, idx[i:]], y, test_size=0.2, random_state=0)
    LR = LogisticRegression().fit(x_train, y_train)

    # 模型预测并计算准确率
    y_pred = LR.predict(x_test)
    acc.append(accuracy_score(y_test, y_pred))

# 绘准确率的折线图
print(acc)
plt.plot(range(0, 10), acc, marker='o')
plt.xlabel('ATTR removed')
plt.ylabel('acc')
plt.ylim(0.7, 0.9)
# plt.show()

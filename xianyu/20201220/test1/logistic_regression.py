import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.metrics import accuracy_score

# 数据读取
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 模型训练
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
LR = LogisticRegression().fit(x_train, y_train)

# 模型预测并计算准确率
y_pred = LR.predict(x_test)
print('真实值', y_test)
print('预测值', y_pred)
print(accuracy_score(y_test, y_pred))

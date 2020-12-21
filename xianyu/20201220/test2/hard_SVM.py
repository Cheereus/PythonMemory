from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

default_colors = ['c', 'g', 'r', 'b', 'k']
X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=0)  # 100个点 2类 2标签
print(X, y)
# x为数据集的feature，y为label.
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 标准化
standardScaler = StandardScaler()
standardScaler.fit(x_train)
X_standard = standardScaler.transform(x_train)

# 硬间隔支持向量机
svc = LinearSVC(C=10**4)
svc.fit(X_standard, y_train)
y_pred = svc.predict(standardScaler.transform(x_test))

# 计算准确率
print(accuracy_score(y_pred, y_test))

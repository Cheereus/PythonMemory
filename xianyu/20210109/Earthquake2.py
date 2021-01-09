# 支持向量机回归
import pandas as pd
from sklearn.svm import LinearSVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt

# 读取文件
raw_data = pd.read_table("quake.dat", sep=",", header=None).values
data = raw_data[:, :3]
data = StandardScaler().fit_transform(data)
labels = raw_data[:, 3]

# 划分训练集与测试集
train_data = data[:2000]
train_label = labels[:2000]
test_data = data[2000:]
test_label = labels[2000:]

# 数据标准化及训练
svm_reg = make_pipeline(StandardScaler(), LinearSVR(random_state=0, tol=1e-5))
svm_reg.fit(train_data, train_label)

# 预测
pred_label = svm_reg.predict(test_data)

# 输出 MSE 和 RMSE
print(mean_squared_error(pred_label, test_label))
print(mean_squared_error(pred_label, test_label, squared=False))

# 画图
plt.scatter(pred_label, test_label, s=10)
# plt.xlim([5.8, 5.9])
plt.show()
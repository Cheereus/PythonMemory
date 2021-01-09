# 线性回归
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# 读取文件
raw_data = pd.read_table("quake.dat", sep=",", header=None).values

# 数据标准化
data = raw_data[:, :3]
data = StandardScaler().fit_transform(data)
labels = raw_data[:, 3]

# 划分训练集与测试集
train_data = data[:2000]
train_label = labels[:2000]
test_data = data[2000:]
test_label = labels[2000:]

# 训练
linear_reg = LinearRegression().fit(train_data, train_label)

# 预测
pred_label = linear_reg.predict(test_data)

# 输出 MSE 和 RMSE
print(mean_squared_error(pred_label, test_label))
print(mean_squared_error(pred_label, test_label, squared=False))

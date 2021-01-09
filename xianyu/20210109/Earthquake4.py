# 神经网络
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential
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

# 神经网络搭建
batch_size = 1

model = Sequential([
    layers.Dense(8, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
model.compile(loss=keras.losses.MSE, optimizer='adam', metrics=['mse'])

# 训练
model.fit(x=train_data, y=train_label, validation_split=0.1, epochs=20, batch_size=batch_size)

# 预测
pred_label = model.predict(test_data)

# 输出 MSE 和 RMSE
print(mean_squared_error(pred_label, test_label))
print(mean_squared_error(pred_label, test_label, squared=False))

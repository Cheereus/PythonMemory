import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# 读取 txt 文件
def read_from_txt(filePath):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(str, line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    array_data = np.array(data_list)
    return array_data


data = read_from_txt('diabetes.tab.txt')
X = data[1:, 2].astype(np.float32)
y = data[1:, -1].astype(np.float32)

X = [[i] for i in X]
y = [[i] for i in y]

# 数据集划分
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 模型训练
reg = LinearRegression().fit(x_train, y_train)

# 模型预测，输出真实值和预测值
y_pred = reg.predict(x_test)
print('真实值', np.array(y_test).T)
print('预测值', y_pred.T)

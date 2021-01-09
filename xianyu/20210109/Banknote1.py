# 逻辑回归
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score


# Read data from `.txt` file
def read_from_txt(filePath):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(str, line.split(',')))
        data_list.append(num)
        line = f.readline()
    f.close()
    array_data = np.array(data_list)
    return array_data


# 读取数据及预处理
raw_data = read_from_txt('data_banknote_authentication.txt')
data = raw_data[:, :4].astype(float)
data = StandardScaler().fit_transform(data)
labels = raw_data[:, 4]
labels = [int(i[0]) for i in labels]

# 洗牌，不洗牌的话测试集全为一类
np.random.seed(1)
idx = np.arange(len(labels))
np.random.shuffle(idx)
data = data[idx]
labels = np.array(labels)[idx]

# 划分训练集与测试集
train_data = data[:1200]
train_label = labels[:1200]
test_data = data[1200:]
test_label = labels[1200:]

# 训练
clf = LogisticRegression(random_state=0).fit(train_data, train_label)

# 预测
pred_label = clf.predict(test_data)

# 输出 precision 及 recall
print(precision_score(test_label, pred_label))
print(recall_score(test_label, pred_label))

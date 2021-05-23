import numpy as np
from tqdm import trange
import joblib

window_size = [23430, 19360, 19488, 19452, 19797, 21105, 18897, 18920, 19361, 17241, 18972, 18045, 21158, 19882, 19275,
               18838, 18931, 18743]
c = 18
f = open('data/data_chr' + str(c) + '.txt', encoding='utf-8')
lines = f.readlines()
data = []
line_id = 1

# 清洗数据，后续操作只处理 chr 和 pos，并保存原序号
for line in lines:
    line = list(map(str, line.split()))
    # print(len(line))
    data.append([line_id, line[0], line[6], line[7]])
    line_id += 1

data = np.array(data)
# 按第3列排序
data = data[data[:, 2].astype('int64').argsort()]

window = window_size[c - 1]
w_id = 0
w_start = w_id * window
w_end = (w_id + 1) * window

print('Loading database of chr', c)
database = joblib.load('database/Chr' + str(c) + '.pkl')
database = np.array([list(map(str, line.split())) for line in database])
print(data[-1])
print(database[-1])






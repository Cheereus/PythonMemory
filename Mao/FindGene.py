# coding=utf-8
import xlrd
import numpy as np
from tqdm import trange

# 俩文件路径
databasePath = 'chr9.txt'
excelPath = 'chr9.xlsx'

# 从 excel 中读取基因所在染色体及位置
x1 = xlrd.open_workbook(excelPath)
sheet = x1.sheets()
Chr, POS = sheet[0].col_values(0), sheet[0].col_values(1)

Chr = np.array([str(int(i)) for i in Chr[1:]])
POS = np.array([int(i) for i in POS[1:]])
ids = np.argsort(Chr, kind='stable')
Chr = Chr[ids]
POS = POS[ids]

# 从 database 中读取所有基因
f = open(databasePath)
line = f.readline()
data_list = []
line_id = 0
# while line:
#     if line[0] != '#':
#         line_data = list(map(str, line.split()))
#         data_list.append(line_data)
#     line = f.readline()
#     line_id += 1
#     if line_id % 10000:
#         print('Reading', line_id)

# 查找
n = len(Chr)
result_list = []

for i in trange(n):
    c, p = Chr[i], POS[i]
    while True:
        if len(line) <= 0:
            print(line_id)
            break
        if line[0] != '#':
            line_data = list(map(str, line.split()))
            chr_str = line_data[0].split('r')

            if len(chr_str) <= 1:
                line = f.readline()
                line_id += 1
                continue
            if str(c) != chr_str[1]:
                if c == '9':
                    print(i, line + 'axiba', chr_str[1])
                line = f.readline()
                line_id += 1
                continue
            if p < int(line_data[1]):
                break
            if str(c) == chr_str[1] and p == int(line_data[1]):
                result_list.append(line_data)
                line = f.readline()
                line_id += 1
                break
        line = f.readline()
        line_id += 1
f.close()

# 写入文件
output = open('result.txt', 'a')
for result in result_list:
    output.writelines(' '.join(result) + '\n')
output.close()





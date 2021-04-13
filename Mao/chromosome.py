'''
Description: 
Author: CheeReus_11
Date: 2020-08-18 09:26:48
LastEditTime: 2020-08-20 09:50:04
LastEditors: CheeReus_11
'''

import numpy as np


# Read data from `.txt` file
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


data = read_from_txt('data/maf.txt')

# 按第五列排序
data = data[data[:, 4].astype('int64').argsort()]

print(data.shape)

# 窗口大小
window_size = 500000

f = open('../Application/data/result_chr.txt', 'a')

# 这里偷懒了，应该先按染色体把原数据分开再分别遍历的
for i in range(1, 20):

    # 当前最大值和最大行
    tmp_max = 0
    max_line = []

    # 窗口索引
    group = 1

    # 遍历每一行
    for line in data:

        chromosome = int(line[1])
        location = int(line[4])
        value = float(line[3])

        if chromosome == i:

            # 在每进入下一个窗口的时候，将前一个窗口的最大值写入文件
            if location >= group * window_size:
                print(chromosome)
                if tmp_max != 0:
                    f.writelines(' '.join(max_line) + '\n')
                group += 1
                tmp_max = 0
            if value > tmp_max:
                # 更新最大值和最大
                tmp_max = value
                max_line = line

    f.writelines(' '.join(max_line) + '\n')

f.close()

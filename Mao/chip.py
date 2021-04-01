import numpy as np
from tqdm import trange


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


data = read_from_txt('DDLLYYMAF.txt')

# 按第三列排序
# data = data[data[:,2].astype('int64').argsort()]

data = data[1:]
print(data.shape)
print('开始读取数据：')

chromosome_id = 1
min_position = [int(data[0][3])]
max_position = []
genes = []

tmp_list = []

for i in trange(len(data)):
    CHR, SNP, SCORE, POS = data[i]
    if int(CHR) == chromosome_id:
        tmp_list.append([SNP, float(SCORE), int(POS)])
    if int(CHR) != chromosome_id:
        genes.append(tmp_list)
        chromosome_id += 1
        min_position.append(int(POS))
        max_position.append(int(data[i - 1][3]))
        tmp_list = [[SNP, float(SCORE), int(POS)]]

    if i == len(data) - 1:
        genes.append(tmp_list)
        max_position.append(int(POS))

# print(min_position)
# print(max_position)
# print([len(i) for i in genes])

# 18个N
N_list = [388, 199, 177, 176, 137, 193, 164, 181, 189, 95, 108, 76, 269, 189, 193, 106, 85, 75]
# 18个窗口大小
Window_list = []
for i in range(len(N_list)):
    Window_list.append((max_position[i] - min_position[i]) / N_list[i])

print(Window_list)

max_score_list = []
for i in range(len(N_list)):

    tmp_max = genes[i][0]
    # 窗口索引
    group = 1
    # 窗口大小
    window_size = Window_list[i]
    tmp_max_score_list = []
    for gene in genes[i]:
        SNP, SCORE, POS = gene
        if POS >= group * window_size + min_position[i]:
            if tmp_max[1] > 0:
                tmp_max_score_list.append([i + 1] + tmp_max)
            group += 1
            tmp_max = ['', 0, 0]
        if SCORE > tmp_max[1]:
            tmp_max = [SNP, SCORE, POS]

    if tmp_max[1] > 0:
        tmp_max_score_list.append([i + 1] + tmp_max)
    max_score_list.append(tmp_max_score_list)

#
# print(max_score_list[0])
print([len(i) for i in max_score_list])

f = open('result.txt', 'a')

for max_scores in max_score_list:
    for max_score in max_scores:
        max_score = [str(i) for i in max_score]
        f.writelines(' '.join(max_score) + '\n')

f.close()

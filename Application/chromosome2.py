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
    # 去表头
    array_data = np.array(data_list[1:])
    return array_data


data = read_from_txt('data/CFJY_YY_LD.txt')

# 窗口大小
window_size = 1000000
# 窗口索引
group = 1
# 当前基因
current_gene = data[0]
# 相关系数和
r2_sum = 0
# 同在一个窗口内的B基因数目
b_num = 0
# 计数君
t = 1

f = open('data/result_chr.txt', 'a')

for item in data:

    CHR_A = int(item[0])
    BP_A = int(item[1])
    BP_B = int(item[4])
    r2 = float(item[-1])
    # print(CHR_A, BP_A, t)
    t += 1

    # 开始下一个染色体前重置窗口，并写入上一个染色体的最后一个基因
    if CHR_A > int(current_gene[0]):
        if b_num == 0:
            r2_avg = 0
        else:
            r2_avg = r2_sum / b_num
        f.writelines(' '.join([current_gene[0], current_gene[2], current_gene[1], str(r2_avg)]) + '\n')
        current_gene = item
        group = 1

    # 窗口滑动时更新当前基因，重置当前相关系数和，并加入结果
    if BP_A >= group * window_size:
        if b_num == 0:
            r2_avg = 0
        else:
            r2_avg = r2_sum / b_num
        print(current_gene)
        f.writelines(' '.join([current_gene[0], current_gene[2], current_gene[1], str(r2_avg)]) + '\n')
        group += 1
        r2_sum = 0
        b_num = 0
        current_gene = item

    # 对满足条件的B基因进行加和
    if BP_B < group * window_size:
        r2_sum += r2
        b_num += 1

# 写入最后一条
if b_num == 0:
    r2_avg = 0
else:
    r2_avg = r2_sum / b_num
f.writelines(' '.join([current_gene[0], current_gene[2], current_gene[1], str(r2_avg)]) + '\n')

f.close()



from tqdm import trange
import numpy as np

excel_source = 'quchong_sex_int.txt'
Seq_XY = 'Seq_XY.txt'

f = open(excel_source, encoding='utf-8')
lines = f.readlines()
f.close()
data_excel = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    data_excel.append(line)
data_excel = np.array(data_excel)
print(data_excel.shape)
ID = data_excel[:, 3]

f = open(Seq_XY, encoding='utf-8')
data_Seq = f.readlines()
f.close()

result_list = []
for i in range(len(data_Seq)):
    line = list(map(str, data_Seq[i].split()))
    chr_idx_1 = np.where(ID == line[2])[0]
    if chr_idx_1.size > 0:
        SRC = data_excel[chr_idx_1, -1]
        if len(SRC) > 0:
            line[5] = SRC[0]
        else:
            print(line)
    print(line)
    result_list.append(line)


output = open('SexWithSrc.txt', 'w', encoding='utf-8')
for result in result_list:
    output.writelines(' '.join([result[0], result[1], result[2], result[3], result[4], result[5], result[6]]) + '\n')
output.close()




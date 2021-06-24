from tqdm import trange
import numpy as np

f = open('Reverse.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_all = []
data_all_dict = {}
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    data_all.append(line)
    data_all_dict[line[2]] = i


f = open('My_over.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_over = []
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    # print(line[0])
    if line[0] in data_all_dict:
        data_over.append(data_all[data_all_dict[line[0]]])

print(len(data_over))


output = open('My_over_detail.txt', 'w', encoding='utf-8')
for result in data_over:
    output.writelines(' '.join(result) + '\n')
output.close()

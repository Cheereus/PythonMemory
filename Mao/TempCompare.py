from tqdm import trange
import numpy as np
import time

f = open('SamePos/xinyun.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_xinyun = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split(',')))
    data_xinyun.append(line)
data_xinyun = np.array(data_xinyun)
time.sleep(0.5)
print(data_xinyun.shape)
time.sleep(0.5)

name_dict = {}
pos_dict = {}
for i in trange(data_xinyun.shape[0]):
    name_dict[data_xinyun[i][0]] = i
    pos_dict[data_xinyun[i][1]] = i
# print(name_dict, pos_dict)

f = open('temp/ASA_S20210500001.tab', encoding='utf-8')
lines = f.readlines()
f.close()
data_temp = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    data_temp.append(line[0:1] + [line[1] + ':' + line[2]] + line[3:])
data_temp = np.array(data_temp)
time.sleep(0.5)
print(data_temp.shape)
time.sleep(0.5)

asa_out = open('temp/no.txt', 'w', encoding='utf-8')
count1 = 0
count2 = 0
counts = 0
for i in trange(data_temp.shape[0]):
    pos_name, chr_pos = data_temp[i][0], data_temp[i][1]
    # print(pos_name, chr_pos)
    pos_idx = -1
    if chr_pos in pos_dict:
        counts += 1
        count1 += 1
        pos_idx = pos_dict[chr_pos]
    elif pos_name in name_dict:
        counts += 1
        count2 += 1
        pos_idx = name_dict[pos_name]
    else:
        pass
    if pos_idx < 0:
        asa_out.writelines(','.join(data_temp[i]) + '\n')
asa_out.close()
print(count1, count2, counts)

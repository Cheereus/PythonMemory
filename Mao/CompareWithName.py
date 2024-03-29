from tqdm import trange
import numpy as np
import time

f = open('temp/NewXinyun.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_xinyun = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split(',')))
    data_xinyun.append([line[1] + ':' + line[2].split('.')[0]] + line[3:])
data_xinyun = np.array(data_xinyun)
# xinyun_pos_name = data_xinyun[:, 0]
# xinyun_chr_pos = data_xinyun[:, 1]

f = open('NewASA.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_asa = []
for i in trange(len(lines)):
    if 'UU' not in lines[i] and 'DD' not in lines[i] and 'II' not in lines[i]:
        line = list(map(str, lines[i].split(',')))
        data_asa.append(line)
data_asa = np.array(data_asa)
# print(data_asa.shape)
name_pos = {}
for i in trange(data_asa.shape[0]):
    name_pos[data_asa[i][1] + ':' + data_asa[i][2]] = i

time.sleep(0.5)
print('Comparing')
time.sleep(0.5)
asa_out = open('SamePos/asa.txt', 'w', encoding='utf-8')
xinyun_out = open('SamePos/xinyun.txt', 'w', encoding='utf-8')
count1 = 0
count2 = 0
counts = 0
for i in trange(data_xinyun.shape[0]):
    chr_pos = data_xinyun[i][0]
    pos_idx = -1

    if chr_pos in name_pos:
        counts += 1
        count1 += 1
        pos_idx = name_pos[chr_pos]
    else:
        pass
    if pos_idx >= 0:
        xinyun_out.writelines(','.join(data_xinyun[i]))
        asa_out.writelines(','.join(data_asa[pos_idx]))
xinyun_out.close()
asa_out.close()
print(counts, count1, count2)




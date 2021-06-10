from tqdm import trange
import numpy as np
import time

f = open('xinyun.csv', encoding='utf-8')
lines = f.readlines()[1:]
f.close()
data_xinyun = []
for i in trange(len(lines)):
    line = list(map(str, lines[i][:-1].split(',')))
    data_xinyun.append(line[0:1] + [line[1] + ':' + line[2]] + line[3:])
data_xinyun = np.array(data_xinyun)
xinyun_pos_name = data_xinyun[:, 0]
xinyun_chr_pos = data_xinyun[:, 1]

f = open('asa(1).txt', encoding='utf-8')
lines = f.readlines()[1:]
f.close()
data_asa = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    data_asa.append(line)
data_asa = np.array(data_asa)
name_pos = {}
for i in trange(data_asa.shape[0]):
    name_pos[data_asa[i][0]] = i

time.sleep(0.5)
print('Comparing')
time.sleep(0.5)
asa_out = open('SamePos/asa.txt', 'w', encoding='utf-8')
xinyun_out = open('SamePos/xinyun.txt', 'w', encoding='utf-8')
count1 = 0
count2 = 0
counts = 0
for i in trange(data_xinyun.shape[0]):
    pos_name, chr_pos = data_xinyun[i][0], data_xinyun[i][1]
    pos_idx = -1

    # if chr_pos in name_pos:
    #     counts += 1
    #     count1 += 1
    #     pos_idx = name_pos[chr_pos]
    if pos_name in name_pos:
        counts += 1
        count2 += 1
        pos_idx = name_pos[pos_name]
    else:
        pass
    if pos_idx >= 0:
        xinyun_out.writelines(','.join(data_xinyun[i]) + '\n')
        asa_out.writelines(','.join(data_asa[pos_idx]) + '\n')
xinyun_out.close()
asa_out.close()
print(counts, count1, count2)




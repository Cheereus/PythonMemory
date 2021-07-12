# coding=utf-8
from tqdm import trange
import numpy as np

same_counts = 0
HNXD_counts = 0
CFJY_counts = 0

f = open('HNXD_YY_767_qc.bim', encoding='utf-8')
lines = f.readlines()
f.close()
HNXD = {}
HNXD_list = []
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    HNXD[CHR + ':' + POS] = ID
    HNXD_list.append([CHR, POS, ID])

f = open('CFJY_YY_4789_qc.bim', encoding='utf-8')
lines = f.readlines()
f.close()
output_same = open('same_pos.lst', 'w', encoding='utf-8')
output_CFJY = open('CFJY_pos.lst', 'w', encoding='utf-8')
CFJY = {}

for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    CFJY[CHR + ':' + POS] = ID
    if CHR + ':' + POS in HNXD:
        output_same.writelines(' '.join([HNXD[CHR + ':' + POS], ID]) + '\n')
        same_counts += 1
    else:
        output_CFJY.writelines(' '.join([ID]) + '\n')
        CFJY_counts += 1

output_same.close()
output_CFJY.close()

output_HNXD = open('HNXD_pos.lst', 'w', encoding='utf-8')
for i in trange(len(HNXD_list)):
    CHR, POS, ID = HNXD_list[i]
    if CHR + ':' + POS in CFJY:
        pass
    else:
        output_HNXD.writelines(' '.join([ID]) + '\n')
        HNXD_counts += 1

output_HNXD.close()

print('Same:', same_counts)
print('CFJY:', CFJY_counts)
print('HNXD:', HNXD_counts)

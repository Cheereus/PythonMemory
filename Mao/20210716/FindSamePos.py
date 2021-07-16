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
output_same_CFJY = open('common_CFJY.lst', 'w', encoding='utf-8')
output_same_HNXD = open('common_HNXD.lst', 'w', encoding='utf-8')
output_CFJY = open('CFJY_pos.lst', 'w', encoding='utf-8')
CFJY = {}

same_dict = {}

for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    CFJY[CHR + ':' + POS] = ID

    if CHR + ':' + POS in HNXD:
        output_same_CFJY.writelines(' '.join([ID]) + '\n')
        output_same_HNXD.writelines(' '.join([HNXD[CHR + ':' + POS]]) + '\n')
        same_dict[HNXD[CHR + ':' + POS]] = ID
        same_counts += 1  # 最终 12304
    else:
        output_CFJY.writelines(' '.join([ID]) + '\n')
        CFJY_counts += 1

output_same_CFJY.close()
output_same_HNXD.close()
output_CFJY.close()

output_HNXD = open('HNXD_pos.lst', 'w', encoding='utf-8')
HNXD_same_counts = 0
for i in trange(len(HNXD_list)):
    CHR, POS, ID = HNXD_list[i]
    if CHR + ':' + POS in CFJY:
        HNXD_same_counts += 1  # 最终 12305
        # if ID not in same_dict:
        #     print(ID)
    else:
        output_HNXD.writelines(' '.join([ID]) + '\n')
        HNXD_counts += 1

output_HNXD.close()

print('Same:', same_counts)
print('CFJY:', CFJY_counts)
# print('HNXD_same:', HNXD_same_counts)
print('HNXD:', HNXD_counts)

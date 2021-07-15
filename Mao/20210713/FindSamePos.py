# coding=utf-8
from tqdm import trange
import numpy as np

same_counts = 0
SHQN_counts = 0
CFJY_counts = 0

f = open('SHQN_YY_7159_qc.bim', encoding='utf-8')
lines = f.readlines()
f.close()
SHQN = {}
SHQN_list = []
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    SHQN[CHR + ':' + POS] = ID
    SHQN_list.append([CHR, POS, ID])

f = open('CFJY_YY_4789_qc.bim', encoding='utf-8')
lines = f.readlines()
f.close()
output_same_CFJY = open('common_CFJY.lst', 'w', encoding='utf-8')
output_same_SHQN = open('common_SHQN.lst', 'w', encoding='utf-8')
output_CFJY = open('CFJY_pos.lst', 'w', encoding='utf-8')
CFJY = {}

same_dict = {}

for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    CFJY[CHR + ':' + POS] = ID

    if CHR + ':' + POS in SHQN:
        output_same_CFJY.writelines(' '.join([ID]) + '\n')
        output_same_SHQN.writelines(' '.join([SHQN[CHR + ':' + POS]]) + '\n')
        same_dict[SHQN[CHR + ':' + POS]] = ID
        same_counts += 1  # 最终 12304
    else:
        output_CFJY.writelines(' '.join([ID]) + '\n')
        CFJY_counts += 1

output_same_CFJY.close()
output_same_SHQN.close()
output_CFJY.close()

output_SHQN = open('SHQN_pos.lst', 'w', encoding='utf-8')
SHQN_same_counts = 0
for i in trange(len(SHQN_list)):
    CHR, POS, ID = SHQN_list[i]
    if CHR + ':' + POS in CFJY:
        SHQN_same_counts += 1  # 最终 12305
        # if ID not in same_dict:
        #     print(ID)
    else:
        output_SHQN.writelines(' '.join([ID]) + '\n')
        SHQN_counts += 1

output_SHQN.close()

print('Same:', same_counts)
print('CFJY:', CFJY_counts)
print('SHQN_same:', SHQN_same_counts)
print('SHQN:', SHQN_counts)

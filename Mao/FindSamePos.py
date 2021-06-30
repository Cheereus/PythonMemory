# coding=utf-8
from tqdm import trange
import numpy as np

f = open('HNXD_YY_767_correct.bim', encoding='utf-8')
lines = f.readlines()
f.close()
HNXD = {}
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    HNXD[CHR + ':' + POS] = ID

f = open('CFJY_YY_4789_correct.bim', encoding='utf-8')
lines = f.readlines()
f.close()
output = open('same_pos.lst', 'w', encoding='utf-8')
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS, ID = line[0], line[3], line[1]
    if CHR + ':' + POS in HNXD:
        output.writelines(' '.join([HNXD[CHR + ':' + POS], ID]) + '\n')
output.close()

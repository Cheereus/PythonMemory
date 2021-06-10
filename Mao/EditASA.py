from tqdm import trange
import numpy as np
import time


f = open('ASA-24v1-0_A1.csv', encoding='utf-8')
lines = f.readlines()[1:]
f.close()
data_ASA_2 = {}
for i in trange(len(lines)):
    line = list(map(str, lines[i].split(',')))
    NAME, ILMNSTR, CHR, POS = line[1], line[2], line[9], line[10]
    data_ASA_2[NAME] = ':'.join([ILMNSTR, CHR, POS])

f = open('asa(1).txt', encoding='utf-8')
lines = f.readlines()[1:]
f.close()
output = open('NewASA.txt', 'w', encoding='utf-8')
count = 0
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    NAME = line[0]
    if NAME in data_ASA_2:
        count += 1
        ILMNSTR, CHR, POS = data_ASA_2[NAME].split(':')
        output.writelines(','.join([ILMNSTR, CHR, POS] + line) + '\n')

output.close()

print('Found', len(lines), '/', count)

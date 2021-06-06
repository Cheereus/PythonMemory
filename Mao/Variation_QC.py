import numpy as np
from tqdm import trange


f = open('structural_variations.gvf', encoding='utf-8')
lines = f.readlines()
result_list = []
last_line = ['0', '0', '0']

for i in trange(len(lines)):
    line = lines[i]
    if '##' not in line:
        line = list(map(str, line.split()))
        CHR, START, END = line[0], line[3], line[4]
        if CHR == last_line[0] and START == last_line[1] and END == last_line[2]:
            continue
        if int(START) - int(END) <= 1000000:
            result_list.append([CHR, START, END])
        last_line = [CHR, START, END]

print(len(result_list), '/', len(lines))
print(len(result_list) / len(lines))

output = open('QC_Variation_1M.txt', 'w', encoding='utf-8')
for result in result_list:
    output.writelines(' '.join(result) + '\n')

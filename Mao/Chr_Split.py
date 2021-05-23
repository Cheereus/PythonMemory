import xlrd
from collections import Counter
from tqdm import trange

f = open('quchong3_int.txt', encoding='utf-8')
lines = f.readlines()
line_nums = len(lines)
f.close()
Chr = list(range(1, 19)) + ['X', 'Y']
print(Chr)

for c in Chr:
    output = open('data/data_chr' + str(c) + '.txt', 'a', encoding='utf-8')
    for i in trange(line_nums):
        line = list(map(str, lines[i].split()))
        if str(c) == line[6]:
            output.writelines(' '.join(line) + '\n')
    output.close()

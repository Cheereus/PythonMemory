# coding=utf-8
import joblib
from tqdm import trange
databasePath = 'snpdatabse.vcf'

f = open(databasePath)
lines = f.readlines()
chromosomes = [str(i) for i in list(range(1, 19))] + ['X', 'Y']
total = 0
chr_dict = {}
for chr_ in chromosomes:
    chr_dict[chr_] = []

for i in trange(len(lines)):
    line = lines[i]
    if len(line) > 0 and line[0] != '#':
        line_data = list(map(str, line.split()))
        chr_str = line_data[0].split('r')
        for chr_ in chromosomes:
            if chr_str[1] == chr_:
                chr_dict[chr_].append(line_data)
                break

# 写入 .pkl 文件
for chr_ in chromosomes:
    print(len(chr_dict[chr_]))
    joblib.dump(chr_dict[chr_], 'database/Chr' + chr_ + '.pkl')


f.close()

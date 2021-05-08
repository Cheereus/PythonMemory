# coding=utf-8
import joblib
databasePath = 'snpdatabse.vcf'

f = open(databasePath)
lines = f.readlines()
# print('chr1\t' in lines[40])
print(len(lines))
chromosomes = [str(i) for i in list(range(1, 19))] + ['X', 'Y']
total = 0
for chr_ in chromosomes:
    chr_lines = [line for line in lines if len(line) > 0 and line[0] != '#' and ('chr'+chr_+'\t') in line]
    print(len(chr_lines))
    total += len(chr_lines)
    # 写入 .pkl 文件
    joblib.dump(chr_lines, 'database/Chr' + chr_ + '.pkl')

print(total)
f.close()

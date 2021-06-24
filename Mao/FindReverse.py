# coding=utf-8
# samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr1:1111-1111
import subprocess
from tqdm import trange
import numpy as np

f = open('CFJY_YY_4789_freq.frq', encoding='utf-8')
lines = f.readlines()[1:]
f.close()
data_freq = []
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    data_freq.append(line)

data_freq = np.array(data_freq)
f = open('CFJY_YY_4789.map', encoding='utf-8')
lines = f.readlines()
f.close()
data_map = []
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    data_map.append(line)

data_map = np.array(data_map)

result_list = []
for i in range(data_map.shape[0]):
    freq = data_freq[i]
    map_ = data_map[i]
    if freq[1] == map_[1]:
        result_list.append([freq[1], freq[0], map_[3], freq[2], freq[3], map_[2]])

output = open('CFJY_YY_4789.txt', 'w', encoding='utf-8')
for result in result_list:
    output.writelines(' '.join(result) + '\n')
output.close()

SNP_DICT = {
    'A': 'T',
    'C': 'G',
    'T': 'A',
    'G': 'C',
}
reverse_list = [['chromosome', '0_idx_position', 'snp_name', 'genetic_distance', 'allele_1', 'allele_2', 'reference', 'reference_rev', 'strand']]
hubu = []

for i in trange(len(result_list)):
    ID, CHR, POS, A1, A2, DIS = result_list[i]
    A = A1 + A2
    if '0' not in A and SNP_DICT[A1] == A2:
        hubu.append(result_list[i])
    status, output = subprocess.getstatusoutput('samtools faidx /home/liujf/WORKSPACE/duh/10_2/reference/pig.fa chr' + CHR + ':' + str(POS) + '-' + str(POS))

    if status == 0:
        X = ''.join(output.split('\n')[1:])
        if X in A and SNP_DICT[X] not in A:
            reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], 'forward'])
        else:
            reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], 'reverse'])
    else:
        reverse_list.append([CHR, POS, ID, DIS, A1, A2, '', '', 'ambiguous'])

print(len(reverse_list))
print(len(hubu))
output = open('Reverse.txt', 'w', encoding='utf-8')
output1 = open('Reverse_ID.txt', 'w', encoding='utf-8')
for reverse in reverse_list:
    output.writelines(' '.join(reverse) + '\n')
    if reverse[-1] == 'reverse':
        output1.writelines(reverse[2] + '\n')
output.close()
output1.close()

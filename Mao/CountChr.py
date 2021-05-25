import numpy
from tqdm import trange

f = open('quchong0525.txt', encoding='utf-8')
lines = f.readlines()
count = {}
result_list = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    # print(line)
    line[0] = line[0].split('.')[0]
    line[6] = line[6].split('.')[0]
    line[7] = line[7].split('.')[0]
    chr_id = line[6]
    result_list.append(line)
    if chr_id in count.keys():
        count[chr_id] += 1
    else:
        count[chr_id] = 1

print(count)
print(len(result_list))
output = open('quchong0525_int.txt', 'a', encoding='utf-8')
for result in result_list:
    output.writelines(' '.join(result) + '\n')
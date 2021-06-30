# coding=utf-8
from tqdm import trange


f = open('CFJY_YY_4789_reverse.txt', encoding='utf-8')
lines = f.readlines()
f.close()
CFJY_reverse = []
CFJY_reverse_dict = {}
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    CFJY_reverse.append(line)
    CFJY_reverse_dict[line[2]] = i


f = open('HNXD_YY_767_reverse.txt', encoding='utf-8')
lines = f.readlines()
f.close()
HNXD_reverse = []
HNXD_reverse_dict = {}
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    HNXD_reverse.append(line)
    HNXD_reverse_dict[line[2]] = i


f = open('same_pos.lst', encoding='utf-8')
lines = f.readlines()
f.close()
same_pos_list = {}
for i in range(len(lines)):
    line = list(map(str, lines[i].split()))
    ID1, ID2 = line[0], line[1]
    same_pos_list[ID2] = ID1


output_CFJY = open('MISS_CFJY_YY_4789.txt', 'w', encoding='utf-8')
output_HNXD = open('MISS_HNXD_YY_767.txt', 'w', encoding='utf-8')

f = open('CFJY_YY_4789_HNXD_YY_767.missnp', encoding='utf-8')
lines = f.readlines()
f.close()
for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CFJY_ID = line[0]
    HNXD_ID = same_pos_list[CFJY_ID]
    output_CFJY.writelines(' '.join(CFJY_reverse[CFJY_reverse_dict[CFJY_ID]]) + '\n')
    output_HNXD.writelines(' '.join(HNXD_reverse[HNXD_reverse_dict[HNXD_ID]]) + '\n')


output_CFJY.close()
output_HNXD.close()

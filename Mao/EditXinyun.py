from tqdm import trange
import numpy as np
import time


f = open('forward_strand_YZ01.csv', encoding='utf-8')
lines = f.readlines()[1:]
f.close()

output = open('temp/NewXinyun.txt', 'w', encoding='utf-8')

for i in trange(len(lines)):
    line = lines[i]
    if '"' in line:
        left, mid, right = line.split('"')
        mid = mid.split(',')
        mid = '-'.join(mid)
        line = left + mid + right
    output.writelines(line)

output.close()

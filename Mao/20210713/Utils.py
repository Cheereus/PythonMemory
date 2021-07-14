import numpy as np
from tqdm import trange
import time


def read_file_nd(filePath, head=0):
    print('Reading...', filePath)
    time.sleep(0.5)

    f = open(filePath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    data = []
    for i in trange(head, len(lines)):
        line = lines[i]
        if '#' in line:
            continue
        if '\n' in line:
            line = line.replace('\n', '')
            # print('回车')
        line = list(map(str, line.split()))
        data.append(line)
    data = np.array(data)
    return data


def write_data_to_file(filePath):
    output = open('SamePos/Sample_' + str(i) + '.txt', 'w', encoding='utf-8')
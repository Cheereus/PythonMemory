import numpy as np
from tqdm import trange
import time

Chr = list(range(1, 19)) + ['X', 'Y']
total_count = 0
for c in Chr:

    print('Screening in Chr', c)
    f = open('QC_1MB/QC_Chr' + str(c) + '.txt', encoding='utf-8')
    lines = f.readlines()
    f.close()
    data_variation = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_variation.append(line)
    data_variation = np.array(data_variation)
    print('Loading QC Variation', data_variation.shape)
    variation_nums = data_variation.shape[0]

    f = open('Porcine_Chip/Chr_' + str(c) + '.txt', encoding='utf-8')
    lines = f.readlines()
    f.close()
    data_chip = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_chip.append(line)
    data_chip = np.array(data_chip)
    line_nums = data_chip.shape[0]
    print('Loading Chip Data', data_chip.shape)

    print('Start Screening')
    counts = 0
    output = open('QC_Result/Chr' + str(c) + '.txt', 'w', encoding='utf-8')
    time.sleep(0.5)
    for i in trange(line_nums):
        line = data_chip[i]
        in_variation = 0
        for j in range(variation_nums):
            variation = data_variation[j]
            if int(variation[1]) <= int(line[6]) <= int(variation[2]):
                in_variation = 1
                break
        if in_variation == 0:
            counts += 1
            output.writelines(' '.join(line) + '\n')
    output.close()
    total_count += counts
    print('Chr', c, 'QC Left', counts, '/', line_nums)
    print('----------------------')

time.sleep(0.5)
print('Total QC left', total_count)

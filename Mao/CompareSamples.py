from tqdm import trange
import numpy as np
import time

f = open('SamePos/asa.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_asa = []
for i in trange(len(lines)):
    line = lines[i]
    if '\n' in line:
        line = line.replace('\n', '')
        # print('回车')
    line = list(map(str, line.split(',')))
    data_asa.append(line)
data_asa = np.array(data_asa)

f = open('SamePos/xinyun.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_xinyun = []
for i in trange(len(lines)):
    line = lines[i]
    if '\n' in line:
        line = line.replace('\n', '')
        # print('回车')
    line = list(map(str, line.split(',')))
    data_xinyun.append(line)
data_xinyun = np.array(data_xinyun)
print(data_xinyun.shape)

Reverse_dict = {
    'A': 'T',
    'C': 'G',
    'T': 'A',
    'G': 'C',
}

for i in range(1, 17):
    # print('Comparing', i)
    output = open('SamePos/Sample_' + str(i) + '.txt', 'w', encoding='utf-8')
    output.writelines(' '.join(['asa_id', 'xinyun_id', 'chr', 'pos', 'same', 'asa-genotype', 'xinyun-genotype']) + '\n')
    total = 0
    count = 0
    time.sleep(0.5)
    for j in range(data_xinyun.shape[0]):
        xinyun = data_xinyun[j]
        asa = data_asa[j]
        # print(xinyun[0:1], xinyun[1].split(':'))
        result = [asa[3], xinyun[1], xinyun[0].split(':')[0], xinyun[0].split(':')[1]]
        REF = xinyun[2]
        ALT = xinyun[3].split('-')
        if len(xinyun[i + 3]) == 1:
            xinyun[i + 3] = xinyun[i + 3] + xinyun[i + 3]
        if len(asa[i + 3]) == 1:
            asa[i + 3] = asa[i + 3] + asa[i + 3]
        if len(xinyun[i + 3] + asa[i + 3]) == 4 and '.' not in xinyun[i + 3] + asa[i + 3] and 'I' not in xinyun[i + 3] + asa[i + 3] and 'D' not in xinyun[i + 3] + asa[i + 3] and 'U' not in xinyun[i + 3] + asa[i + 3] and '-' not in xinyun[i + 3] + asa[i + 3]:
            total += 1
            # if asa[0] == 'MINUS' or asa[0] == 'BOT':
            #     tmp = ''
            #     for p in asa[i + 3]:
            #         tmp += Reverse_dict[p]
            #     asa[i + 3] = tmp

            if xinyun[i + 3] == asa[i + 3] or xinyun[i + 3] == asa[i + 3][::-1]:
                count += 1
                result.append('T')
            else:
                tmp = ''
                for p in asa[i + 3]:
                    # print(asa[i + 3])
                    tmp += Reverse_dict[p]
                if xinyun[i + 3] == tmp or xinyun[i + 3] == tmp[::-1]:
                    asa[i + 3] = tmp
                    count += 1
                    result.append('T')
                else:
                    result.append('F')

        result.append(xinyun[i + 3])
        result.append(asa[i + 3])
        if len(result) == 7:
            output.writelines(' '.join(result) + '\n')

    output.close()
    time.sleep(0.5)
    print(i, data_xinyun.shape[0], total, count, count / total)
    # print('均检出', total, '/', data_xinyun.shape[0])
    # print('一致数', count)
    # print('一致率', count / total)
    # print('----------')

from tqdm import trange
import numpy as np
import time

f = open('SamePos/asa.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_asa = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split(',')))
    data_asa.append(line)
data_asa = np.array(data_asa)

f = open('SamePos/xinyun.txt', encoding='utf-8')
lines = f.readlines()
f.close()
data_xinyun = []
for i in trange(len(lines)):
    line = list(map(str, lines[i].split(',')))
    data_xinyun.append(line)
data_xinyun = np.array(data_xinyun)
print(data_xinyun.shape)


for i in range(1, 17):
    print('Comparing', i)
    output = open('SamePos/Sample_' + str(i) + '.txt', 'w', encoding='utf-8')
    total = 0
    count = 0
    time.sleep(0.5)
    for j in trange(data_xinyun.shape[0]):
        xinyun = data_xinyun[j]
        asa = data_asa[j]
        # print(xinyun[0:1], xinyun[1].split(':'))
        result = [xinyun[0], xinyun[1].split(':')[0], xinyun[1].split(':')[1]]
        if len(xinyun[i+1] + asa[i]) == 4 and '-' not in xinyun[i+1] + asa[i]:
            total += 1
            if xinyun[i+1] == asa[i]:
                count += 1
                result.append('T')
            else:
                result.append('F')
        if len(result) == 4:
            output.writelines(' '.join(result) + '\n')

    output.close()
    time.sleep(0.5)
    print('均检出', total)
    print('一致数', count)
    print('一致率', count / total)
    print('----------')

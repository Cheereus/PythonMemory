from tqdm import trange
import numpy as np
import time

Chr = list(range(1, 23)) + ['X', 'Y',]
total_counts = 0

for c in Chr:

    f = open('ASA/Chr' + str(c) + '.txt', encoding='utf-8')
    ASA = f.readlines()
    data_asa = []
    f.close()
    for i in range(len(ASA)):
        line = list(map(str, ASA[i].split(',')))
        data_asa.append(line)
    data_asa = np.array(data_asa)

    f = open('Xinyun/Chr' + str(c) + '.txt', encoding='utf-8')
    Xinyun = f.readlines()
    data_xinyun = []
    f.close()
    for i in range(len(Xinyun)):
        line = list(map(str, Xinyun[i].split(',')))
        data_xinyun.append(line)
    data_xinyun = np.array(data_xinyun)
    POS_xinyun = data_xinyun[:, 2]

    print('Comparing Chr', c)
    print(data_asa.shape, data_xinyun.shape)
    time.sleep(0.5)

    asa_out = open('CompareResult/asa_chr' + str(c) + '.txt', 'w', encoding='utf-8')
    xinyun_out = open('CompareResult/xinyun_chr' + str(c) + '.txt', 'w', encoding='utf-8')
    counts = 0
    for i in trange(data_asa.shape[0]):
        POS = data_asa[i][1]
        xinyun_idx = np.argwhere(POS_xinyun == POS)
        if xinyun_idx.size > 0:
            counts += 1
            if xinyun_idx.size > 1:
                print(data_xinyun[xinyun_idx])
            xinyun_idx = xinyun_idx[0][0]
            asa_out.writelines(','.join(data_asa[i]))
            xinyun_out.writelines(','.join(data_xinyun[xinyun_idx]))

    asa_out.close()
    xinyun_out.close()
    total_counts += counts
    print('Same Pos', counts)
    print('------------------')

print('Total counts', total_counts)




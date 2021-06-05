import joblib
import numpy as np
from tqdm import trange

data = joblib.load('data_correct1.pkl')

f = open('Porcine_chip_120k_提交版.out1')
lines = f.readlines()
f.close()

CHR = data[:, 5]
POS = data[:, 6]

CHR = [i.split('.')[0] for i in CHR]
POS = [i.split('.')[0] for i in POS]

CHR = np.array(CHR)
POS = np.array(POS)

for i in trange(20):
    s = lines[i*6 + 1]
    c, p = s.split(' ')
    p = p.split('\n')[0]
    chr_idx = np.argwhere(POS == p)
    chr_idx = chr_idx[0][0]
    data[chr_idx, 11], data[chr_idx, 12] = data[chr_idx, 12], data[chr_idx, 11]

joblib.dump(data, 'data_correct2.pkl')

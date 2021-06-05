import joblib
import numpy as np
from tqdm import trange

data = joblib.load('data_correct2.pkl')

f = open('Porcine_chip_120k_提交版.out2')
lines = f.readlines()
f.close()

CHR = data[:, 5]
POS = data[:, 6]

CHR = [i.split('.')[0] for i in CHR]
POS = [i.split('.')[0] for i in POS]

CHR = np.array(CHR)
POS = np.array(POS)

for i in trange(58):
    s = lines[i*6]
    up = lines[i*6 + 1].split()[-1]
    down = lines[i*6 + 3].split()[-1]
    c, p, ref, alt, _3 = s.split()
    chr_idx = np.argwhere(POS == p)
    chr_idx = chr_idx[0][0]
    data[chr_idx][4] = up + '[' + ref + '/' + alt + ']' + down

# joblib.dump(data, 'data_correct3.pkl')

output = open('data_correct.txt', 'w', encoding='utf-8')
for result in data:
    result[0] = result[0].split('.')[0]
    result[5] = result[5].split('.')[0]
    result[6] = result[6].split('.')[0]
    output.writelines(' '.join(result) + '\n')
output.close()

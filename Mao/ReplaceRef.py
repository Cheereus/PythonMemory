import xlrd
import numpy as np
from tqdm import trange
import joblib

excelPath = 'Porcine_chip_120k_20210528.xlsx'
x1 = xlrd.open_workbook(excelPath)
sheet = x1.sheets()[0]

data = []
for i in trange(5, sheet.nrows):
    line = sheet.row_values(i)
    data.append(line)
data = np.array(data)
print(data.shape)
count = 0
for i in trange(data.shape[0]):
    line = data[i]
    SEQ, REF, ALT = line[4], line[11], line[12]
    t1 = SEQ.split('[')[1]
    t2 = t1.split(']')[0]
    ref_seq, alt_seq = t2.split('/')
    if ref_seq != REF or alt_seq != ALT:
        data[i][11] = ref_seq
        data[i][12] = alt_seq
        count += 1

print(count)

joblib.dump(data, 'data_correct1.pkl')

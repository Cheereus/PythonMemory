import xlrd
import numpy as np
from tqdm import trange
import joblib

excelPath = 'Porcine_Chip_120k_v1.2.xlsx'
x1 = xlrd.open_workbook(excelPath)
sheet = x1.sheets()[0]

data = []
counts = 0
for i in trange(5, sheet.nrows):
    line = sheet.row_values(i)
    line[0] = str(line[0]).split('.')[0]
    line[5] = str(line[5]).split('.')[0]
    line[6] = str(line[6]).split('.')[0]
    SEQ, REF, ALT = line[4], line[11], line[12]
    SEQ_before, t1 = line[4].split('[')
    t2, SEQ_after = t1.split(']')
    SEQ_ref, SEQ_alt = t2.split('/')
    if SEQ_ref != REF or SEQ_alt != ALT:
        counts += 1
        line[4] = SEQ_before + '[' + REF + '/' + ALT + ']' + SEQ_after
    data.append(line)
data = np.array(data)
print(data.shape)
print(counts)
output = open('QC_ALL.txt', 'w', encoding='utf-8')

for line in data:
    output.writelines(' '.join(line) + '\n')
output.close()


import xlrd
import numpy
from tqdm import trange

x1 = xlrd.open_workbook('SexChr.xlsx')
sheet = x1.sheets()[0]

d = []
for r in trange(sheet.nrows):
    data1 = []
    for c in range(sheet.ncols):
        cell_value = str(sheet.cell_value(r, c))
        if len(cell_value) > 0:
            data1.append(cell_value)
        else:
            data1.append('-')

    d.append(list(data1))

d = numpy.array(d)
CP_list = []
result_list = []

for i in trange(d.shape[0]):
    cp = str(d[i][5]) + '-' + str(d[i][6])
    if cp not in CP_list:
        result_list.append(d[i])
    CP_list.append(cp)


result_list = numpy.array(result_list)

print(result_list.shape)

output = open('quchong_sex.txt', 'w', encoding='utf-8')
for result in result_list:
    output.writelines(' '.join(result) + '\n')

import xlrd
import numpy
from tqdm import trange

x1 = xlrd.open_workbook('quchong2.xlsx')
sheet = x1.sheets()[2]

d = []
for r in trange(5, sheet.nrows):
    data1 = []
    for c in range(sheet.ncols):
        data1.append(sheet.cell_value(r, c))
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

output = open('result_quchong2.txt', 'a')
for result in result_list:
    output.writelines(' '.join(result) + '\n')
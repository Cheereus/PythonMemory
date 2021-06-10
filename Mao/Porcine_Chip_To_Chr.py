import xlrd
import numpy
from tqdm import trange

x1 = xlrd.open_workbook('Porcine_Chip_120k_v1.1.xlsx')
sheet = x1.sheets()[0]

d = []
for r in trange(5, sheet.nrows):
    data1 = []
    for c in range(sheet.ncols):
        cell_value = str(sheet.cell_value(r, c))
        if len(cell_value) > 0:
            data1.append(cell_value)
        else:
            data1.append('-')

    d.append(list(data1))

d = numpy.array(d)
line_nums = d.shape[0]
print(d.shape)

Chr = list(range(1, 19)) + ['X', 'Y']
for c in Chr:
    output = open('Porcine_Chip/Chr_' + str(c) + '.txt', 'w', encoding='utf-8')
    for i in trange(line_nums):
        line = d[i]
        line[0] = line[0].split('.')[0]
        line[5] = line[5].split('.')[0]
        line[6] = line[6].split('.')[0]
        if str(c) == line[5]:
            output.writelines(' '.join(line) + '\n')
    output.close()

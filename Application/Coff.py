# coding=UTF-8
import vcf
import numpy as np
import math

# 读取文件
real_reader = vcf.Reader(filename='data/DD_gt_real_impute_1.vcf')
generate_reader = vcf.Reader(filename='data/DD_MOLO3.0_gt_impute.vcf')


# 获取基因型
def get_gene_type(REF, ALT, VALUE):
    # print(VALUE)
    value1, value2 = VALUE.split('|')
    genetype = ''
    if value1 == '0':
        genetype += REF
    else:
        genetype += str(ALT[0])
    if value2 == '0':
        genetype += REF
    else:
        genetype += str(ALT[0])

    return genetype


# 获取基因型数值
def get_gene_int(REF, ALT, TYPE1, TYPE2):
    type_int_1 = 0
    type_int_2 = 0
    if TYPE1 == (REF + str(ALT[0])) or TYPE1 == (str(ALT[0]) + REF):
        type_int_1 = 1
    if TYPE1 == (REF + REF):
        type_int_1 = 2
    if TYPE2 == (REF + str(ALT[0])) or TYPE2 == (str(ALT[0]) + REF):
        type_int_2 = 1
    if TYPE2 == (REF + REF):
        type_int_2 = 2

    return type_int_1, type_int_2


gene_matrix_1 = []
gene_matrix_2 = []

# 行计数
row = 0

for real, generate in zip(real_reader, generate_reader):

    line_vec_1 = []
    line_vec_2 = []

    for real_sample, generate_sample in zip(real.samples, generate.samples):
        real_gene_type = get_gene_type(real.REF, real.ALT, real_sample[real.FORMAT.split(':')[0]])
        generate_gene_type = get_gene_type(generate.REF, generate.ALT, generate_sample[generate.FORMAT.split(':')[0]])

        type_int = get_gene_int(real.REF, real.ALT, real_gene_type, generate_gene_type)
        line_vec_1.append(type_int[0])
        line_vec_2.append(type_int[1])

    gene_matrix_1.append(line_vec_1)
    gene_matrix_2.append(line_vec_2)

    row += 1
    # 观察进度
    print('row', row, 'finished')

gene_matrix_1 = np.array(gene_matrix_1)
gene_matrix_2 = np.array(gene_matrix_2)
print(gene_matrix_1.shape)
print(gene_matrix_2.shape)


def mean2(x):
    y = np.sum(x) / np.size(x)
    return y


def corr2(a, b):
    a = a - mean2(a)
    b = b - mean2(b)

    r = (a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum())
    return r


print(corr2(gene_matrix_1, gene_matrix_2))

import vcf

# 读取文件
real_reader = vcf.Reader(filename='data/DD_gt_real_impute_1.vcf')
generate_reader = vcf.Reader(filename='data/DD_MOLO3.0_gt_impute.vcf')


# 获取基因型
def get_gene_type(REF, ALT, VALUE):
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


# 每次运行会在文件内追加，所以要记得把上次的运行结果重命名一下
f = open('data/outputs.txt', 'a')

# 行计数，总数，一致数
row = 0
n_samples = 0
all_acc = 0

# 按列计数
accuracy = []
col = 0

for real, generate in zip(real_reader, generate_reader):

    # 写个文件头
    if row == 0:
        headline = ['CHROM', 'POS', 'ID']
        headline += [i.sample for i in real.samples]
        accuracy = [0 for i in real.samples]
        headline += ['ACC']
        f.writelines(' '.join(headline) + '\n')

    # 行内计数、行内一致数
    n_line_samples = 0
    line_acc = 0

    # 把结果拼接成行
    result = [real.CHROM, str(real.POS), real.ID]

    for real_sample, generate_sample in zip(real.samples, generate.samples):

        real_gene_type = get_gene_type(real.REF, real.ALT, real_sample[real.FORMAT.split(':')[0]])
        generate_gene_type = get_gene_type(generate.REF, generate.ALT, generate_sample[generate.FORMAT.split(':')[0]])

        n_line_samples += 1
        n_samples += 1

        if real_gene_type == generate_gene_type or real_gene_type == generate_gene_type[::-1]:
            result.append('1')
            line_acc += 1
            all_acc += 1
            accuracy[col] += 1
        else:
            result.append('0')

        # 列进一
        col += 1

    col = 0

    result.append(str(line_acc / n_line_samples))

    f.writelines(' '.join(result) + '\n')
    row += 1
    # 观察进度
    print('row', row, 'finished')


# 给准确率这行前面加三个词来保持工整
accuracy = ['ACC', 'PER', 'COL'] + [str(round(i / row, 4)) for i in accuracy]
f.writelines(' '.join(accuracy) + '\n')

f.close()

# 最后输出总准确率
print(all_acc / n_samples)

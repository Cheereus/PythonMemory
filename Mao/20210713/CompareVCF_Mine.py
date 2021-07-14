from Utils import *


# 获取基因型
def get_gene_type(REF, ALT, VALUE):
    value1, value2 = VALUE.split('/')
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


# 计算基因型一致性
def get_gene_correction(genetype1, genetype2, standard=1):
    # 标准一，准确率较高
    if standard == 1:
        c = 0
        for idx in range(2):
            if genetype1[idx] == genetype2[idx]:
                c += 1

        if c == 0:
            genetype2 = genetype2[::-1]
            for idx in range(2):
                if genetype1[idx] == genetype2[idx]:
                    c += 1
        return c
    if standard == 2:
        if genetype1 == genetype2 or genetype1 == genetype2[::-1]:
            return 2
        else:
            return 0


real_list = read_file_nd('HNXD_YY_02_gt_real.vcf', head=24)
impute_list = read_file_nd('HNXD_YY_re02_gt_impute.vcf', head=24)

real_list_dict = {}
for real in real_list:
    real_list_dict[real[2]] = real[3:]

correction_list = []
acc_rows = []
sample_nums = len(real_list[0][9:])
std = 2
print('Using standard', std, 'Comparing...')
time.sleep(0.5)
for i in trange(len(impute_list)):
    impute = impute_list[i]
    impute_ID, impute_ref, impute_alt, impute_samples = impute[2], impute[3], impute[4], impute[9:]
    real = real_list_dict[impute_ID]
    # real = real_list[i][3:]
    real_ID, real_ref, real_alt, real_samples = impute_ID, real[0], real[1], real[6:]

    if len(real_samples) != len(impute_samples):
        e = Exception('Sample ERROR')
        raise e

    correction_row = []
    row_correction = []
    for j in range(len(real_samples)):
        real_values = real_samples[j]
        impute_values = impute_samples[j]
        real_genetype = get_gene_type(real_ref, real_alt, real_values)
        impute_genetype = get_gene_type(impute_ref, impute_alt, impute_values)
        sample_correction = get_gene_correction(real_genetype, impute_genetype, standard=std)
        row_correction.append(sample_correction)
        correction_row.append(sample_correction)
    correction_list.append(correction_row)
    acc_rows.append(sum(row_correction) / (2 * sample_nums))

correction_list = np.array(correction_list)
rows, cols = correction_list.shape
acc = np.sum(correction_list) / (rows * cols * 2)
acc_cols = []
for i in range(cols):
    acc_cols.append(np.sum(correction_list[:, i]) / (2 * rows))

print('Total acc :', acc)
print('Gene num  :', len(acc_rows))
print('Sample num:', len(acc_cols))





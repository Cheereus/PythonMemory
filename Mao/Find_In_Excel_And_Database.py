import numpy as np
import joblib
from tqdm import trange

for c in range(1, 19):

    # 读取 excel 数据库
    print('Loading excel of chr', c)
    excel_database = open('data/data_chr' + str(c) + '.txt', encoding='utf-8')
    data_excel = []
    for line in excel_database.readlines():
        line = list(map(str, line.split()))
        line_length = len(line)
        if line_length != 18:
            trait = '-'.join(line[15:line_length - 2])
            line = line[:15] + [trait] + line[-2:]
        data_excel.append(line)
    excel_database.close()
    data_excel = np.array(data_excel)

    # 读取 database
    print('Loading database of chr', c)
    database = joblib.load('database/Chr' + str(c) + '.pkl')
    database = np.array([list(map(str, line.split())) for line in database])
    positions_database = database[:, 1]

    # 读取筛选后位点
    print('Loading points of chr', c)
    f = open('result/Chr_' + str(c) + '.txt', encoding='utf-8')
    point_list = []
    for line in f.readlines():
        line = list(map(str, line.split()))
        point_list.append(line)
    f.close()

    # 每个位点进行查找
    positions_excel = data_excel[:, 7]
    result_list = []
    point_in_excel = 0
    point_in_database = 0
    for i in trange(len(point_list)):
        c, p = point_list[i]
        # 先找 excel
        chr_idx = np.argwhere(positions_excel == p)
        if chr_idx.size > 0:
            chr_idx = chr_idx[0][0]
            result_list.append(data_excel[chr_idx])
            point_in_excel += 1
        else:
            # 再找 database
            chr_idx = np.argwhere(positions_database == p)
            if chr_idx.size > 0:
                chr_idx = chr_idx[0][0]
                result = database[chr_idx]
                # 数据格式保持一致，空白部分先填充占位字符
                result_list.append(['-', 'Sus', 'scrofa', result[2], 'Duroc', 'SEQ', c, p, '-', '-', '-', 'Autosome', result[3], result[4], result[2], '-', '-', 'dbSNP'])
                point_in_database += 1

    result_list = np.array(result_list)
    print('总位点数：', len(point_list))
    print('Excel 位点数：', point_in_excel)
    print('Database 位点数：', point_in_database)
    print('查找结果：', result_list.shape)
    print('----------------')

    # 写入文件
    output = open('find_result/Chr_' + str(c) + '.txt', 'w', encoding='utf-8')
    for result in result_list:
        output.writelines(' '.join(result) + '\n')
    output.close()






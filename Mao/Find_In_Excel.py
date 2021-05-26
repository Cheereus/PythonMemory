import numpy as np

for c in range(1, 19):

    # 读取 excel 数据库
    excel_database = open('data/data_chr' + str(c) + '.txt', encoding='utf-8')
    data_excel = []
    for line in excel_database.readlines():
        line = list(map(str, line.split()))
        data_excel.append(line)
    excel_database.close()
    data_excel = np.array(data_excel)

    # 读取筛选后位点
    f = open('result/Chr_' + str(c) + '.txt', encoding='utf-8')
    point_list = []
    for line in f.readlines():
        line = list(map(str, line.split()))
        point_list.append(line)
    f.close()

    # 每个位点进行查找
    positions = data_excel[:, 6]
    result_list = []
    for point in point_list:
        c, p = point
        chr_idx = np.argwhere(positions == p)
        if chr_idx.size > 0:
            chr_idx = chr_idx[0][0]
            result_list.append(data_excel[chr_idx])





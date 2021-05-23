import numpy as np
from tqdm import trange
import joblib

window_nums = [11709, 7848, 6817, 6730, 5280, 8095, 6448, 7345, 7206, 4023, 4173, 3414, 9847, 7130, 7285, 4244, 3354, 2987]

# window_size = [23430, 19360, 19488, 19452, 19797, 21105, 18897, 18920, 19361, 17241, 18972, 18045, 21158, 19882, 19275,
#                18838, 18931, 18743]

sum_result = 0
sum_no_genes = 0

for c in range(1, 19):

    # c = 18
    f = open('data/data_chr' + str(c) + '.txt', encoding='utf-8')
    lines = f.readlines()
    data = []
    line_id = 1

    # 清洗数据，后续操作只处理 chr 和 pos，并保存原序号
    for line in lines:
        line = list(map(str, line.split()))
        # print(len(line))
        data.append([line_id, line[0], line[6], line[7]])
        line_id += 1

    data = np.array(data)
    # 按第3列排序
    data = data[data[:, 2].astype('int64').argsort()]

    print('Loading database of chr', c)
    database = joblib.load('database/Chr' + str(c) + '.pkl')
    database = np.array([list(map(str, line.split())) for line in database])

    max_length = int(max(data[-1][-1], database[-1][1]))
    windows = window_nums[c - 1]
    window_size = max_length // windows

    positions_1 = data[:, 3].astype('int64')
    positions_2 = database[:, 1].astype('int64')

    # print('Window size:', window_size)
    result_list = []
    no_genes = []

    for w_id in trange(windows):

        w_start = w_id * window_size
        w_end = (w_id + 1) * window_size
        w_center = (w_start + w_end) // 2
        # print(positions)
        chr_idx_1 = np.where((positions_1 >= w_start) & (positions_1 < w_end))[0]

        # quchong 中有
        if len(chr_idx_1) > 0:
            data_window_1 = data[chr_idx_1]
            # 只有一个，直接取
            if len(chr_idx_1) == 1:
                result = data_window_1[0]
                result_list.append(['chr' + str(result[2]), result[3]])

            # 有俩的时候
            elif len(chr_idx_1) == 2:

                if abs(int(data_window_1[0][3]) - int(data_window_1[1][3])) >= (window_size / 2):
                    result = data_window_1[0]
                    result_list.append(['chr' + str(result[2]), result[3]])
                    result = data_window_1[1]
                    result_list.append(['chr' + str(result[2]), result[3]])
                else:
                    # 先按优先级排序
                    data_sort_by_pri = data_window_1[data_window_1[:, 1].argsort(kind='stable')]
                    if data_sort_by_pri[0][1] < data_sort_by_pri[-1][1]:
                        result = data_sort_by_pri[0]
                        result_list.append(['chr' + str(result[2]), result[3]])
                    # 比较与中心的距离
                    else:
                        data_distance = []
                        # 计算中心距离
                        for item in data_sort_by_pri:
                            data_distance.append([item[0], item[1], item[2], abs(int(item[3]) - w_center)])
                        data_distance = np.array(data_distance)
                        # 按中心距离排序
                        data_sort_by_dis = data_sort_by_pri[data_distance[:, 3].argsort(kind='stable')]
                        # 取最小者
                        result = data_sort_by_dis[0]
                        result_list.append(['chr' + str(result[2]), result[3]])

            else:
                # 先按优先级排序
                data_sort_by_pri = data_window_1[data_window_1[:, 1].argsort(kind='stable')]
                min_pri = data_sort_by_pri[0][1]
                max_pri = data_sort_by_pri[-1][1]

                # 如果有两种优先级，只取优先级较小的那部分
                # 只有一种优先级时直接进行中心距离排序
                if min_pri != max_pri:
                    data_sort_by_pri = data_sort_by_pri[np.argwhere(data_sort_by_pri == min_pri)][0]

                data_distance = []
                # 计算中心距离

                # print(data_sort_by_pri.shape)
                for item in data_sort_by_pri:
                    # print(item.shape)
                    data_distance.append([item[0], item[1], item[2], abs(int(item[3]) - w_center)])
                data_distance = np.array(data_distance)
                # 按中心距离排序
                data_sort_by_dis = data_sort_by_pri[data_distance[:, 3].argsort(kind='stable')]
                # 取最小者
                result = data_sort_by_dis[0]
                result_list.append(['chr' + str(result[2]), result[3]])

        # quchong 中没有
        else:

            chr_idx_2 = np.where((positions_2 >= w_start) & (positions_2 < w_end))[0]
            # database 中有
            # database 中不再需要优先级排序
            if len(chr_idx_2) > 0:

                data_window2 = database[chr_idx_2]
                # 只有一个，直接取
                if len(chr_idx_1) == 1:
                    result = data_window2[0]
                    result_list.append([result[0], result[1]])
                else:
                    data_distance = []
                    # 计算中心距离
                    for item in data_window2:
                        data_distance.append([item[0], abs(int(item[1]) - w_center)])
                    data_distance = np.array(data_distance)
                    # 按中心距离排序
                    data_sort_by_dis = data_window2[data_distance[:, 1].argsort(kind='stable')]
                    # 取最小者
                    result = data_sort_by_dis[0]
                    result_list.append([result[0], result[1]])

            # database 中没有
            else:
                no_genes.append([str(w_id), str(w_start), str(w_end)])

    sum_result += len(result_list)
    sum_no_genes += len(no_genes)
    print(len(result_list), windows - len(result_list))

    output = open('result/Chr_' + str(c) + '.txt', 'w')
    for result in result_list:
        output.writelines(' '.join(result) + '\n')
    output.close()

    output = open('result/Chr_' + str(c) + '_No_Gene_Window.txt', 'w')
    for no_gene in no_genes:
        output.writelines(' '.join(no_gene) + '\n')
    output.close()

print('最终位点个数：', sum_result)







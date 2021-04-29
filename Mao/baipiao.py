import matplotlib.pyplot as plt
import numpy as np

data_types = ['DD', 'LL', 'YY']

default_colors = [[138/256, 158/256, 202/256], [246/256, 140/256, 99/256], [98/256, 194/256, 164/256]]

label_dict = {'DD': 'Duroc', 'LL': 'Landrace', 'YY': 'Yorkshire'}


def read_from_txt(filePath, head=False):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(float, line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    # 去表头
    if head:
        data_list = data_list[1:]
    else:
        pass
    array_data = np.array(data_list)
    return array_data


fig = plt.figure(figsize=(15, 75))

for i in range(len(data_types)):
    data = read_from_txt('data/data_' + data_types[i] + '.txt')

    x = ['300', '500', '800', '1k', '1.5k', '2k', '3k']

    print(data)

    plt.subplot(1, 3, i+1)
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    l1 = plt.plot(x, data[:, 0], 'r-', label='Method 1', marker='s', color=default_colors[i])
    l2 = plt.plot(x, data[:, 1], 'g--', label='Method 2', marker='o', color=default_colors[i])
    l3 = plt.plot(x, data[:, 2], 'b-.', label='Method 3', marker='^', color=default_colors[i])

    if i == 0:
        plt.ylabel('Concordance Rate', fontsize=15)
    plt.xlabel('Number of SNPs in LD panel', fontsize=15)

    plt.grid(alpha=0.3)
    plt.legend(fontsize=15)
    plt.ylim(0.8, 1.0)
plt.show()

# 文章中需要用到矢量图
fig.savefig('images/baipiao_CR.svg', dpi=600, format='svg', bbox_inches='tight')
# 普通图片
fig.savefig('images/baipiao_CR.png')

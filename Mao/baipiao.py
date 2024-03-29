import matplotlib.pyplot as plt
import numpy as np

methods = ['SE', 'CR', 'CC', 'GS']

y_lim_start = {'SE': 0, 'CR': 0.8, 'CC': 0.4, 'GS': 0.0}
y_lim_end = {'SE': 3000, 'CR': 1.0, 'CC': 1.0, 'GS': 0.25}

data_types = ['DD', 'LL', 'YY']

default_colors = [[138/256, 158/256, 202/256], [246/256, 140/256, 99/256], [98/256, 194/256, 164/256]]

label_dict = {'DD': 'Duroc', 'LL': 'Landrace', 'YY': 'Yorkshire', 'SE': 'Shanon Entropy', 'CR': 'Concordance Rate', 'CC': 'Correlation Coefficient', 'GS': 'GS Accuracy'}


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


method = 'GS'
trait = 'AGE'


fig = plt.figure(figsize=(15, 75))

for i in range(len(data_types)):
    data = read_from_txt('data/data_' + method + '_' + data_types[i] + '_' + trait +  '.txt')

    x = ['300', '500', '800', '1k', '1.5k', '2k', '3k']

    plt.subplot(1, 3, i+1)
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    l1 = plt.plot(x, data[:, 0], 'r-', label='Method 1', marker='s', color=default_colors[i])
    l2 = plt.plot(x, data[:, 1], 'g--', label='Method 2', marker='o', color=default_colors[i])
    l3 = plt.plot(x, data[:, 2], 'b-.', label='Method 3', marker='^', color=default_colors[i])

    if i == 0:
        plt.ylabel(label_dict[method], fontsize=15)
    plt.xlabel('Number of SNPs in LD panel', fontsize=15)
    plt.title(label_dict[data_types[i]], fontsize=15)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=15, loc=4)
    plt.ylim(y_lim_start[method], y_lim_end[method])
# plt.suptitle('Correlation Coefficient (AGE) of GEBV using raw and imputed LD-chip', y=0.94, fontsize=20)
plt.show()

# 文章中需要用到矢量图
fig.savefig('images/baipiao_' + method + '_' + trait + '.svg', dpi=600, format='svg', bbox_inches='tight')
# 普通图片
fig.savefig('images/baipiao_' + method + '_' + trait + '.png', bbox_inches='tight')

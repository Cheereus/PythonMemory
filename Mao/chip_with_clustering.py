import numpy as np
from tqdm import trange
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

# 改成在开头设置文件，方便改，毛毛就不用跑到代码里找了
input_file = 'DDLLYYMAF.txt'
output_file = 'result.txt'


# 根据染色体号从文件中读取，是个笨方法
def read_from_txt(filePath, chr=1):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(str, line.split()))
        if num[0] == str(chr):
            data_list.append([num[0], num[1], float(num[2]), int(num[3])])
        line = f.readline()
    f.close()
    array_data = np.array(data_list)
    return array_data


# 位点数目，自动考虑开头结尾
N_list = [259, 133, 118, 117, 90, 129, 110, 121, 126, 63, 72, 50, 179, 126, 129, 71, 57, 50]
N_list = [_ - 2 for _ in N_list]
out_f = open(output_file, 'a')


# 开始，增加进度条方便暗中观察 -.-
for chr_id in trange(1, 19):
    data = read_from_txt(input_file, chr=chr_id)

    N = N_list[chr_id - 1]
    first = data[0]
    last = data[-1]
    out_f.writelines(' '.join(first) + '\n')
    # GMM = GaussianMixture(n_components=N, random_state=0).fit(data[:, -1].reshape((-1,1)))
    # labels = GMM.predict(data[:, -1].reshape((-1,1)))
    km = KMeans(n_clusters=N, random_state=0).fit(data[1:-1, -1].reshape((-1, 1)))
    labels = km.labels_
    max_score_list = [[]] * N
    for i in range(N):
        group = []
        for j in range(len(labels)):
            if labels[j] == i:
                group.append(data[1:-1][j])
        tmp_max = group[0]
        for gene in group:
            if gene[2] > tmp_max[2]:
                tmp_max = gene
        max_score_list[i] = tmp_max

    max_score_list = np.array(max_score_list)
    a = [int(_) for _ in max_score_list[:, 3].T]
    a = np.array(a)
    max_score_list = max_score_list[np.argsort(a), :]
    for max_score in max_score_list:
        max_score = [str(i) for i in max_score]
        out_f.writelines(' '.join(max_score) + '\n')
    out_f.writelines(' '.join(last) + '\n')

out_f.close()

# daisuki

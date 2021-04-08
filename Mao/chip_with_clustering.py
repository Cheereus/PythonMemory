import numpy as np
from tqdm import trange
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture


# Read data from `.txt` file
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

N_list = [40,20,18,18,14,19,16,18,19,9,11,7,27,19,19,11,8,7]
N_list = [_ - 2 for _ in N_list]
# print(max_score_list)
f = open('result.txt', 'a')
for chr_id in range(1, 19):
    data = read_from_txt('DDLLYYMAF.txt', chr=chr_id)

    N = N_list[chr_id - 1]
    first = data[0]
    last = data[-1]
    f.writelines(' '.join(first) + '\n')
    # GMM = GaussianMixture(n_components=N, random_state=0).fit(data[:, -1].reshape((-1,1)))
    # labels = GMM.predict(data[:, -1].reshape((-1,1)))
    km = KMeans(n_clusters=N, random_state=0).fit(data[1:-1, -1].reshape((-1,1)))
    labels = km.labels_
    # print(min(labels), max(labels))
    max_score_list = [[]] * N
    for i in range(N):
        group = []
        for j in range(len(labels)):
            if labels[j] == i:
                group.append(data[1:-1][j])
        # print(i, [_ for _ in labels if _ == i])
        tmp_max = group[0]
        for gene in group:
            if gene[2] > tmp_max[2]:
                tmp_max = gene
        max_score_list[i] = tmp_max

    max_score_list = np.array(max_score_list)
    a = [int(_) for _ in max_score_list[:, 3].T]
    a = np.array(a)
    max_score_list = max_score_list[np.argsort(a), :]
    print(max_score_list)
    for max_score in max_score_list:
        max_score = [str(i) for i in max_score]
        f.writelines(' '.join(max_score) + '\n')
    f.writelines(' '.join(last) + '\n')

f.close()
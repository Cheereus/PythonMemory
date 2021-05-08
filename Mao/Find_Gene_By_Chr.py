import joblib
from tqdm import trange
import numpy as np
import time


def find_gene(gene_list, chr_):
    database = joblib.load('database/Chr' + chr_ + '.pkl')
    database = np.array([list(map(str, line.split())) for line in database])
    positions = database[:, 1]
    gene_len = len(gene_list)
    result_list = []
    print('Start finding in chr', chr_)
    time.sleep(1)
    found = 0
    for i in trange(gene_len):
        c, p = gene_list[i]
        chr_idx = np.argwhere(positions == p)
        if chr_idx.size > 0:
            found += 1
            chr_idx = chr_idx[0][0]
            result_list.append(database[chr_idx, :])
        else:
            result_list.append(['chr' + c, p])
    print('Found', found, 'in chr', chr_)
    time.sleep(1)
    return result_list


if __name__ == '__main__':

    data = joblib.load('database/Chr12.pkl')
    data = np.array([list(map(str, line.split())) for line in data])
    data = data[:, 1]
    print(data)
    print(np.argwhere(data == '257096974'))

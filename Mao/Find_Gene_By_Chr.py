import joblib
from tqdm import trange
import numpy as np
import time


def find_closest(pos, database_list):
    positions = database_list[:, 1]
    positions = [abs(int(pos) - int(i)) for i in positions]
    positions = np.array(positions)

    chr_idx = positions.argsort(kind='stable')[0]
    return chr_idx


def find_gene(gene_list, chr_, key_id=1):
    print('Loading database of chr', chr_)
    database = joblib.load('database/Chr' + chr_ + '.pkl')
    database = np.array([list(map(str, line.split())) for line in database])
    positions = database[:, key_id]
    # print(positions)
    gene_len = len(gene_list)
    result_list = []
    print('Start finding in chr', chr_)
    time.sleep(1)
    found = 0
    for i in trange(gene_len):
        # c, p, id_u = gene_list[i]
        c, p, r, a = gene_list[i]
        # if key_id == 1:
        #     search_key = p
        # if key_id == 2:
        # search_key = id_u.split('-')[1]
        # print(search_key)
        chr_idx = np.argwhere(positions == p)
        if chr_idx.size > 0:
            found += 1
            chr_idx = chr_idx[0][0]
            if r == database[chr_idx, 3] and a == database[chr_idx, 4]:
                # result_list.append(['chr' + c, p, id_u] + [database[chr_idx, 2], database[chr_idx, 3], database[chr_idx, 4]])
                result_list.append(['chr' + c, p] + [database[chr_idx, 2], database[chr_idx, 3], database[chr_idx, 4], '-'])
            else:
                chr_idx = find_closest(p, database)
                c, p, id_, r, a = database[chr_idx]
                result_list.append([c, p, id_, r, a, 'dbSNP'])

        else:
            chr_idx = find_closest(p, database)
            c, p, id_, r, a = database[chr_idx]
            result_list.append([c, p, id_, r, a, 'dbSNP'])
    print('Found', found, 'in chr', chr_)
    time.sleep(1)
    return result_list


if __name__ == '__main__':

    data = joblib.load('database/Chr12.pkl')
    data = np.array([list(map(str, line.split())) for line in data])
    data = data[:, 1]
    print(data)
    print(np.argwhere(data == '257096974'))

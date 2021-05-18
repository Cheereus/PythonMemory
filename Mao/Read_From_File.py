import xlrd
from collections import Counter
from tqdm import trange


def read_genes_by_chr_txt(txtPath, withHead=False):
    f = open(txtPath, encoding='utf-8')
    lines = f.readlines()
    f.close()
    Chr = []
    POS = []
    ID_U = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        chr_id = str(line[0]).split('r')[1]
        if len(chr_id) > 3:
            continue
        Chr.append(chr_id)
        POS.append(str(int(line[1])))
        ID_U.append(line[2])

    count_result = Counter(Chr)
    chromosomes = count_result.keys()
    chr_dict = {}

    for chr_ in chromosomes:
        chr_dict[chr_] = []
    for i in range(len(Chr)):
        c, p, id_u = Chr[i], POS[i], ID_U[i]
        c, p = Chr[i], POS[i]
        for chr_ in chromosomes:
            if c == chr_:
                chr_dict[chr_].append([c, p, id_u])
                # chr_dict[chr_].append([c, p])
                break
    return chr_dict


def read_genes_by_chr_xslx(excelPath, withHead=False):
    # 从 excel 中读取基因所在染色体及位置
    x1 = xlrd.open_workbook(excelPath)
    sheet = x1.sheets()
    Chr, POS = sheet[0].col_values(0), sheet[0].col_values(1)
    if withHead:
        Chr = [str(i).split('.')[0] for i in Chr[1:]]
        POS = [str(int(i)) for i in POS[1:]]
    else:
        Chr = [str(i).split('.')[0] for i in Chr]
        POS = [str(int(i)) for i in POS]

    count_result = Counter(Chr)
    chromosomes = count_result.keys()
    chr_dict = {}
    for chr_ in chromosomes:
        chr_dict[chr_] = []
    for i in trange(len(Chr)):
        c, p = Chr[i], POS[i]
        for chr_ in chromosomes:
            if c == chr_:
                chr_dict[chr_].append([c, p])
                break

    # total = 0
    # print(len(Chr))
    # for chr_ in chromosomes:
    #     total += len(chr_dict[chr_])
    #     print(len(chr_dict[chr_]))
    # print(total)
    return chr_dict


if __name__ == '__main__':
    cd = read_genes_by_chr_txt('NQ_11_1.txt')
    print(cd['1'][0])


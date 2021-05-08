import xlrd
from collections import Counter
from tqdm import trange


def read_genes_by_chr(excelPath):
    # 从 excel 中读取基因所在染色体及位置
    x1 = xlrd.open_workbook(excelPath)
    sheet = x1.sheets()
    Chr, POS = sheet[0].col_values(0), sheet[0].col_values(1)
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
    cd = read_genes_by_chr('part1.xlsx')
    print(cd.keys())


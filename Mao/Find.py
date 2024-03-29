from Read_From_File import read_genes_by_chr_xslx, read_genes_by_chr_txt
from Find_Gene_By_Chr import find_gene


def find_gene_of_xlsx(origin, target, withHead):

    cd = read_genes_by_chr_xslx(origin, withHead=withHead)
    # print(cd.keys())
    output = open(target, 'a')
    for key in cd.keys():
        result_list = find_gene(cd[key], key)
        for result in result_list:
            output.writelines(' '.join(result) + '\n')

    output.close()


def find_gene_of_txt(origin, target, withHead):

    cd = read_genes_by_chr_txt(origin, withHead=withHead)
    # print(cd.keys())
    output = open(target, 'w', encoding='utf-8')
    for key in cd.keys():
        result_list = find_gene(cd[key], key, 1)
        for result in result_list:
            output.writelines(' '.join(result) + '\n')

    output.close()


if __name__ == '__main__':
    find_gene_of_txt('quchong_sex_int.txt', 'sex_find.txt', withHead=False)

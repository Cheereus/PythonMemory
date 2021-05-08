from Read_From_Xlsx import read_genes_by_chr
from Find_Gene_By_Chr import find_gene


def find_gene_of_xlsx(origin, target):

    cd = read_genes_by_chr(origin)
    # print(cd.keys())
    output = open(target, 'a')
    for key in cd.keys():
        result_list = find_gene(cd[key], key)
        for result in result_list:
            output.writelines(' '.join(result) + '\n')

    output.close()


if __name__ == '__main__':
    find_gene_of_xlsx('part2.xlsx', 'result_part2.txt')
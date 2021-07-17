# coding=utf-8
# samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr1:1111-1111
import subprocess
from tqdm import trange
import numpy as np
import sys


def find_reverse(file_name):

    f = open(file_name + '.bim', encoding='utf-8')
    lines = f.readlines()
    f.close()
    result_list = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        result_list.append([line[1], line[0], line[3], line[4], line[5], line[2]])

    SNP_DICT = {
        'A': 'T',
        'C': 'G',
        'T': 'A',
        'G': 'C',
    }
    reverse_list = [['chromosome', '0_idx_position', 'snp_name', 'genetic_distance', 'allele_1', 'allele_2', 'reference', 'reference_rev', 'strand']]
    # hubu = []

    for i in trange(len(result_list)):
        strand = 'ambiguous'
        ID, CHR, POS, A1, A2, DIS = result_list[i]
        # if '0' not in A and SNP_DICT[A1] == A2:
        #     hubu.append(result_list[i])
        status, output = subprocess.getstatusoutput('samtools faidx /home/liujf/WORKSPACE/duh/10_2/reference/pig.fa chr' + CHR + ':' + str(POS) + '-' + str(POS))

        if status == 0:
            A1_ = '' + A1
            A2_ = '' + A2
            X = ''.join(output.split('\n')[1:]).upper()

            # 两个位点都是0：ambiguous
            if A1_ == '0' and A2_ == '0' and X != 'N':
                strand = 'ambiguous'
                reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], strand])
            elif A1_ == 'N' or A2_ == 'N' or X == 'N':
                strand = 'forward'
                reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, X, strand])
            else:
                # 将带 0 的处理成纯合位点
                if A1 == '0' and A2 != '0':
                    A1_ = A2
                    A2_ = A2
                if A2 == '0' and A1 != '0':
                    A1_ = A1
                    A2_ = A1
                A = A1_ + A2_

                # 杂合位点
                if A1_ != A2_:
                    # 有REF，判断为正义
                    if X in A:
                        strand = 'forward'
                    # 无REF，判断为反义
                    else:
                        strand = 'reverse'

                # 纯合位点
                else:
                    # 既不是REF也不是REF的互补，判断为正义
                    if X != A1_ and X != SNP_DICT[A1_]:
                        strand = 'forward'
                    # 是REF，判断为正义
                    if X == A1_:
                        strand = 'forward'
                    # 是REF的互补，判断为反义
                    if X == SNP_DICT[A1_]:
                        strand = 'reverse'
                reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], strand])
        else:
            # if X in A and SNP_DICT[X] not in A:
            #     reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], 'forward'])
            # else:
            #     reverse_list.append([CHR, POS, ID, DIS, A1, A2, X, SNP_DICT[X], 'reverse'])
            reverse_list.append([CHR, POS, ID, DIS, A1, A2, '', '', strand])

    print(len(reverse_list))
    # print(len(hubu))
    output = open(file_name + '_reverse.txt', 'w', encoding='utf-8')
    output1 = open(file_name + '_reverse_ID.txt', 'w', encoding='utf-8')
    output2 = open(file_name + '_ambiguous_ID.txt', 'w', encoding='utf-8')
    for reverse in reverse_list:
        output.writelines(' '.join(reverse) + '\n')
        if reverse[-1] == 'reverse':
            output1.writelines(reverse[2] + '\n')
        if reverse[-1] == 'ambiguous':
            output2.writelines(reverse[2] + '\n')
    output.close()
    output1.close()
    output2.close()


if __name__ == '__main__':
    f_name = sys.argv[1]
    find_reverse(f_name)

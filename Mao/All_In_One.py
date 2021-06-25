# coding=utf-8
import sys
import subprocess
from tqdm import trange
import numpy as np
import sys


def replace_sex(file_name, X_id, Y_id):

    f = open(file_name + '.map', encoding='utf-8')
    lines = f.readlines()
    f.close()
    data_map = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        if line[0] == X_id:
            line[0] = 'X'
        if line[0] == Y_id:
            line[0] = 'Y'
        data_map.append(line)

    output = open(file_name + '.map', 'w', encoding='utf-8')
    for result in data_map:
        output.writelines(' '.join(result) + '\n')
    output.close()


def find_reverse(file_name):

    f = open(file_name + '_freq.frq', encoding='utf-8')
    lines = f.readlines()[1:]
    f.close()
    data_freq = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_freq.append(line)

    data_freq = np.array(data_freq)
    f = open(file_name + '.map', encoding='utf-8')
    lines = f.readlines()
    f.close()
    data_map = []
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_map.append(line)

    data_map = np.array(data_map)

    result_list = []
    for i in range(data_map.shape[0]):
        freq = data_freq[i]
        map_ = data_map[i]
        if freq[1] == map_[1]:
            if freq[0] == '19':
                freq[0] = 'X'
            if freq[0] == '20':
                freq[0] = 'Y'
            result_list.append([freq[1], freq[0], map_[3], freq[2], freq[3], map_[2]])

    output = open(file_name + '.txt', 'w', encoding='utf-8')
    for result in result_list:
        output.writelines(' '.join(result) + '\n')
    output.close()

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
            X = ''.join(output.split('\n')[1:])

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


def compare_reverse(file_name):

    f = open(file_name + '_reverse_ID.txt', encoding='utf-8')
    lines = f.readlines()
    f.close()
    data_my = []
    data_my_over = []
    data_my_dict = {}
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_my.append(line)
        # print(line[0])
        data_my_dict[line[0]] = True

    # print(data_my_dict)
    f = open(file_name + '.reverse', encoding='utf-8')
    lines = f.readlines()[1:]
    f.close()
    data_flip = []
    data_flip_over = []
    data_flip_dict = {}
    count = 0
    for i in range(len(lines)):
        line = list(map(str, lines[i].split()))
        data_flip_dict[line[0]] = True
        data_flip.append(line[0])
        # print(line[0])
        if line[0] in data_my_dict.keys():
            count += 1
        else:
            data_flip_over.append(line[0])

    print('Snpflip 有但咱没有：', len(data_flip_over))

    count = 0
    for i in range(len(data_my)):
        ID = data_my[i][0]
        if ID in data_flip_dict.keys():
            count += 1
        else:
            data_my_over.append(ID)

    print('咱有但是 Snpflip 没有：', len(data_my_over))

    output = open(file_name + '_snpflip_over.txt', 'w', encoding='utf-8')
    for result in data_flip_over:
        output.writelines(result + '\n')
    output.close()

    output = open(file_name + '_us_over.txt', 'w', encoding='utf-8')
    for result in data_my_over:
        output.writelines(result + '\n')
    output.close()


if __name__ == '__main__':

    f, X_id, Y_id = sys.argv[1], sys.argv[2], sys.argv[3]

    replace_sex(f, X_id, Y_id)

    cmd1 = 'module load plink'
    cmd2 = 'plink --file $chip --make-bed --out $chip'
    cmd3 = 'python3 /home/liujf/WORKSPACE/maorh/snpflip/snpflip-0.0.6/bin/snpflip -b $chip.bim -f /home/liujf/WORKSPACE/duh/10_2/reference/pig.fa -o $chip'
    cmd4 = 'plink --file $chip --freq --out $chip_freq'

    # cmd = ' && '.join([cmd1, cmd2, cmd3, cmd4]).replace('$chip', file_name)

    for cmd in [cmd1, cmd2, cmd3, cmd4]:
        cmd = cmd.replace('$chip', f)
        print('------------------')
        print('running:', cmd)
        res = subprocess.run(args=cmd, shell=True, check=True)

    print('------------------')
    print('finding...')
    find_reverse(f)
    print('comparing...')
    compare_reverse(f)
    print('filtering...')
    cmd5 = 'plink --file $chip --flip $chip_reverse.txt --exclude $chip_ambiguous_ID.txt --make-bed --out $chip_correct'
    subprocess.run(args=cmd5.replace('$chip', f), shell=True, check=True)

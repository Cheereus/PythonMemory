# coding=utf-8
import sys


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
    file_name = sys.argv[1]
    compare_reverse(file_name)

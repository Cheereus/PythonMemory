# coding=utf-8
import sys
import numpy as np


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


if __name__ == '__main__':
    file_name, X_id, Y_id = sys.argv[1], sys.argv[2], sys.argv[3]
    replace_sex(file_name, X_id, Y_id)

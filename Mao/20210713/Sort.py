from Utils import read_file_nd
import numpy as np

data = read_file_nd('SHQN_id.txt')

SHQN = []

for line in data:
    SHQN.append([line[0], line[1][:7], int(line[1][7:9]), line[1][9:]])

SHQN = np.array(SHQN)

SHQN_sorted = SHQN[SHQN[:, 2].argsort()]

print(SHQN_sorted)

output = open('result.txt', 'w', encoding='utf-8')
for line in SHQN_sorted:
    output.writelines(' '.join([line[0], line[1] + str(line[2]) + line[3]]) + '\n')
output.close()

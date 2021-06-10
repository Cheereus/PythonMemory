from tqdm import trange

f = open('xinyun.csv', encoding='utf-8')
lines = f.readlines()[1:]
line_nums = len(lines)
f.close()
Chr = list(range(1, 23)) + ['X', 'Y', 'MT']
print(Chr)

for c in Chr:
    output = open('Xinyun/Chr' + str(c) + '.txt', 'w', encoding='utf-8')
    for i in trange(line_nums):
        line = list(map(str, lines[i].split(',')))
        # print(line[0])
        #
        CHR = line[1]
        if str(c) == CHR:
            output.writelines(','.join(line))

        # if len(line[0].split(':')) == 2:
        #     CHR, POS = line[0].split(':')
        #     if str(c) == CHR:
        #         output.writelines(','.join([CHR, POS] + line[1:]) + '\n')
    output.close()

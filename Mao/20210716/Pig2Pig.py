from tqdm import trange

f = open('pig10.2.fna')
lines = f.readlines()
f.close()

chromosomes = [str(i) for i in range(1, 19)] + ['X', 'Y']

output = open('new_pig10.2.fna', 'w', encoding='utf-8')
for i in trange(len(lines)):
    line = lines[i]
    if '>' not in line:
        pass
    else:
        line_split = line.split(',')
        chr = line_split[0][-1]
        if chr in chromosomes:
            line = '>chr' + chr + '\n'
    output.writelines(line)
output.close()

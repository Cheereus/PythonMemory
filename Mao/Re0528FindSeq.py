# coding=utf-8
# samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr1:1111-1111
import subprocess
from tqdm import trange


source = 're_0528.txt'
target = 'refind_re_0528.txt'

f = open(source, encoding='utf-8')
lines = f.readlines()
f.close()
result_lines = []

o_file = open(target, 'a', encoding='utf-8')

for i in trange(len(lines)):
    line = list(map(str, lines[i].split()))
    CHR, POS = line[5], int(line[6])

    status, output = subprocess.getstatusoutput('samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa ' + CHR + ':' + str(POS - 100) + '-' + str(POS + 100))
    POS = str(POS)
    origin_seq = ''.join(output.split('\n')[1:])
    Seq_1 = ''
    Seq_2 = ''
    SEQ = ''
    REF_C = ''
    ALT_C = ''
    if status == 0:
        Seq_1 = origin_seq[:100]
        Seq_2 = origin_seq[101:]
        REF_C = origin_seq[100]
        # print(len(origin_seq), len(Seq_1), len(Seq_2), REF_C)
        if len(line) >= 5:
            REF, ALT = line[11], line[12]
            if REF == REF_C:
                ALT_C = ALT
            else:
                ALT_C = REF
            SEQ = Seq_1 + '[' + REF_C + '/' + ALT_C + ']' + Seq_2

            o_file.writelines(' '.join(line[:5] + [SEQ] + line[5:]) + '\n')
        # else:
        #     o_file.writelines(' '.join([CHR, POS, '', '', '', origin_seq]) + '\n')

o_file.close()

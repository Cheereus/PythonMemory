# coding=utf-8
# samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr1:1111-1111
import subprocess
from tqdm import trange
import xlrd


source = 'part1.xlsx'
target = 'part1_result.txt'

x1 = xlrd.open_workbook(source)
sheet = x1.sheets()
CHRS, POSES = sheet[0].col_values(0), sheet[0].col_values(1)
result_lines = []

o_file = open(target, 'a')

for i in trange(len(CHRS)):
    CHR, POS = str(int(CHRS[i])), int(POSES[1])
    status, output = subprocess.getstatusoutput('samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr' + CHR + ':' + str(POS - 100) + '-' + str(POS + 100))
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
        print(len(origin_seq), len(Seq_1), len(Seq_2), REF_C)
        if len(line) >= 5:
            REF, ALT, ID = line[2], line[3], line[4]
            if REF == REF_C:
                ALT_C = ALT
            else:
                ALT_C = REF
            SEQ = Seq_1 + '[' + REF_C + '/' + ALT_C + ']' + Seq_2

            o_file.writelines(' '.join([CHR, POS, ID, REF_C, ALT_C, SEQ]) + '\n')
        else:
            o_file.writelines(' '.join([CHR, POS, '', '', '', origin_seq]) + '\n')

o_file.close()

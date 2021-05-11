# coding=utf-8
# samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr1:1111-1111
import subprocess
from tqdm import trange
import xlrd


source = 'partx.xlsx'
target = 'partx_result.txt'

x1 = xlrd.open_workbook(source)
sheet = x1.sheets()
LATINS, IDS, SPES, CHRS, POSES, REFS, ALTS = sheet[0].col_values(0), sheet[0].col_values(1), sheet[0].col_values(2), sheet[0].col_values(3), sheet[0].col_values(4), sheet[0].col_values(9), sheet[0].col_values(10)

CHRS = [str(i).split('.')[0] for i in CHRS]
result_lines = []

o_file = open(target, 'a')

for i in trange(len(LATINS)):
    LATIN, ID, SPE, CHR, POS, REF, ALT = LATINS[i], IDS[i], SPES[i], CHRS[i], int(POSES[i]), REFS[i], ALTS[i]

    status, output = subprocess.getstatusoutput('samtools faidx /home/liujf/WORKSPACE/duh/11_1/reference/pig.fa chr' + CHR + ':' + str(POS - 100) + '-' + str(POS + 100))
    POS = str(POS)
    origin_seq = ''.join(output.split('\n')[1:])
    Seq_1 = ''
    Seq_2 = ''
    REF_C = ''
    ALT_C = ''
    if status == 0:
        Seq_1 = origin_seq[:100]
        Seq_2 = origin_seq[101:]
        if len(origin_seq) < 100:
            o_file.writelines(' '.join([LATIN, ID, SPE, CHR, POS, '', '', '']) + '\n')
            continue
        REF_C = origin_seq[100]
        if REF == REF_C:
            ALT_C = ALT
        else:
            ALT_C = REF
        SEQ = Seq_1 + '[' + REF_C + '/' + ALT_C + ']' + Seq_2

        o_file.writelines(' '.join([LATIN, ID, SPE, CHR, POS, REF_C, ALT_C, SEQ]) + '\n')

o_file.close()

# coding=utf-8
import sys
from FindReverse import find_reverse
from CompareReverse import compare_reverse
from ReplaceSex import replace_sex
import subprocess

file_name, X_id, Y_id = sys.argv[1], sys.argv[2], sys.argv[3]

replace_sex(file_name, X_id, Y_id)

cmd1 = 'module load plink'
cmd2 = 'plink --file $chip --make-bed --out $chip'
cmd3 = 'python3 /home/liujf/WORKSPACE/maorh/snpflip/snpflip-0.0.6/bin/snpflip -b $chip.bim -f /home/liujf/WORKSPACE/duh/10_2/reference/pig.fa -o $chip'
cmd4 = 'plink --file $chip --freq --out $chip_freq'

# cmd = ' && '.join([cmd1, cmd2, cmd3, cmd4]).replace('$chip', file_name)

for cmd in [cmd1, cmd2, cmd3, cmd4]:
    cmd = cmd.replace('$chip', file_name)
    print('------------------')
    print('running:', cmd)
    res = subprocess.run(args=cmd, shell=True, check=True)


print('------------------')
print('finding...')
find_reverse(file_name)
print('comparing...')
compare_reverse(file_name)
print('filtering...')
cmd5 = 'plink --file $chip --flip $chip_reverse.txt --exclude $chip_ambiguous.txt --make-bed --out $chip_correct'
subprocess.run(args=cmd5.replace('$chip', file_name), shell=True, check=True)
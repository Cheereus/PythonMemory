import re
zeros = 0
f = open('ped1.txt','r+', encoding='UTF-8')
all_lines = f.readlines()
f.seek(0)
f.truncate()
for line in all_lines:
    zero = re.search(r"\b0\b", line)
    if zero:
        zeros = zeros + 1
    line = re.sub(r"\b0\b", 'NA', line)
    f.write(line)
f.close()
print("被替换的0数：" + str(zeros))
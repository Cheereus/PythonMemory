n, k = [10, 1]
happy_str = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1'
happy = [int(i) for i in happy_str.strip().split(' ')]
happy_val = 0
i = 0
tmp_val = 0
happy.sort(reverse=True)
for hi in happy:
    i += 1
    tmp_val += hi
    if i == 3:
        i = 0
        if k + tmp_val >= 0:
            happy_val += (k + tmp_val)
            tmp_val = 0

if tmp_val > 0:
    happy_val += tmp_val

print(happy_val)

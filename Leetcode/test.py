n, k = [10, 5]
happy_str = '1 1 1 1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'
happy = [int(i) for i in happy_str.strip().split(' ')]
happy_val = 0
i = 0
tmp_val = 0
happy.sort(reverse=True)
for hi in happy:
    if hi >= 0:
        i += 1
        tmp_val += hi
        if i == 3:
            i = 0
            happy_val += (k + tmp_val)
            tmp_val = 0
    if hi < 0:
        i += 1
        tmp_val += hi
        if i == 3:
            i = 0
            if k + tmp_val > 0:
                happy_val += (k + tmp_val)
                tmp_val = 0
            else:
                break

print(happy_val)

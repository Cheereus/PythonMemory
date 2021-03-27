n, k = [10, 5]
happy_str = '1 1 1 1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'.rstrip().split(' ')
happy_val = 0
happy = []
i = 0
tmp_val = 0
for hi in happy_str:
    hi = int(hi)
    if hi < 0:
        happy.append(hi)
    if hi >= 0:
        i += 1
        tmp_val += hi
        if i == 3:
            i = 0
            happy_val += (k + tmp_val)
            tmp_val = 0

happy.sort(reverse=True)
for hi in happy:
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

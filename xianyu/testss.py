sum_cur = n
height = 1
while sum_cur <= maxSum:
    floor_sum = 2 * height - 1
    floor_sum = min(index, floor_sum // 2) + min(n - index - 1, floor_sum // 2) + 1
    sum_cur += floor_sum
    height += 1
return height - 1
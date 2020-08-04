'''
Description: 
Author: 陈十一
Date: 2020-08-04 10:06:11
LastEditTime: 2020-08-04 10:18:01
LastEditors: 陈十一
'''

n = int(input("请输入天数"))

# 根据 1 + 2 + ... + x = n, 由等差数列求和公式，反推满足小于等于 n 的最大 x
x = (int(pow(8 * n + 1, 0.5)) - 1) // 2

# 薪水
salary = 0

# 对每个 x, 直接求天数 x 乘以这x天的工资 x*100
for i in range(1, x + 1):
  salary = salary + i * i * 100
  n = n - i

# 上述算法可能会遗留几天没算，补上
salary = salary + n * (x + 1) * 100

print(salary)
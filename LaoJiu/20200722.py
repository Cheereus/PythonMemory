'''
@Description: 
@Author: 陈十一
@Date: 2020-07-22 10:06:12
@LastEditTime: 2020-07-22 10:55:18
@LastEditors: 陈十一
'''
n = 0
sum = 0

# 直接求出所有数的次方备用
pows = [pow(i, 5) for i in range(10)]

# 最大只能有六位数
for i in range(10, 999999):

  # 使用 n 暂存 i
  n = i
  # 每次循环前要把和置零
  sum = 0

  while n != 0:

    # 取余求次方
    sum = sum + pows[n % 10]
    # 取整进位
    n = n // 10
    # 和已经超出就不必再算了
    if sum > i:
      break

  if sum == i:
    print(sum)



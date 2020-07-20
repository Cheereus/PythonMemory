'''
@Description: 
@Author: 陈十一
@Date: 2020-07-20 10:00:06
@LastEditTime: 2020-07-20 10:28:11
@LastEditors: 陈十一
'''

# 通过遍历检查整除来获得全部因子
def allFactor(n):
  fList = [] # 定义一个列表存放因子
  for i in range(1, n): # 遍历整除
    if n % i == 0:
      fList.append(i) # 如果是因子就加进列表
      continue
    else:
      pass
  return fList

# 判断是否为完数
def isWanshu(num):
  factors = allFactor(num)

  # 如果因子的和等于自身则为完数，并将其打印出来
  if num != 0 and num == sum(factors):
    tmp = ""
    for i in range(len(factors)):
      tmp = tmp + str(factors[i])
      if i != len(factors) - 1:
        tmp = tmp + "+"
    tmp = tmp + "=" + str(num)
    print(tmp)

print("请输入N：")

N = int(input())

for i in range(0,N):
  isWanshu(i)
  

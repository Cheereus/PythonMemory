'''
@Description: 
@Author: 陈十一
@Date: 2020-07-31 10:06:23
@LastEditTime: 2020-07-31 10:17:05
@LastEditors: 陈十一
'''

# 想到 7 月 20 号作业也是关于因子的问题，于是借鉴了该作业的内容进行了修改
# 通过遍历检查整除来获得 n 的 m 以内全部因子数目，并输出其奇偶性
def factors(n, m):
  fNum = 0 # 因子数
  for i in range(1, m + 1): # 遍历整除
    if n % i == 0:
      fNum = fNum + 1
      continue
    else:
      pass
  return fNum % 2

n = int(input("请输入灯数："))
m = int(input("请输入人数："))

# 对于每盏灯，根据因子数目的奇偶性判断最终的状态，输出最终打开的灯，即因子数为奇数的灯

for i in range(1, n + 1):
  if factors(i, m) == 1:
    print(i)





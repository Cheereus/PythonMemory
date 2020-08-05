'''
Description: 
Author: 陈十一
Date: 2020-08-05 10:04:04
LastEditTime: 2020-08-05 10:17:21
LastEditors: 陈十一
'''

n = int(input("请输入人数："))
inputStr = input("请输入战斗力：")

# 获取战斗力 list
combat = inputStr.split(" ")
combat = [int(i) for i in combat]

# 计数器
t = 0

# 判断输入合法性
if n % 2 == 0 and len(combat) == n:

  # 对战力进行排序
  combat.sort()
  
  # 按顺序进行两两配对，计算差值并求和
  for i in range(0, n - 1, 2):
    t = t + combat[i + 1] - combat[i]
  print("还需要", t, "次战斗")
  
else:
  print("输入有误！")

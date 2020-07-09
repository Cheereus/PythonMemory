'''
@Description: 
@Author: 陈十一
@Date: 2020-07-09 09:57:03
@LastEditTime: 2020-07-09 10:47:06
@LastEditors: 陈十一
'''
import random

# 提示和用户输入
print("请输入剪刀(V)石头(G)布(W)：")
user = input()

# 两个字典，一个记录输入对应的克星，一个用于输出文字
hands = {"V":"G", "G":"W", "W":"V"}
chinese = {"V":"剪刀", "G":"石头", "W":"布"}

if user in hands:
  
  # AI随机出拳
  ai = random.choice(list(hands))
  
  # 输出对决状况
  print("你出了：", chinese[user], "AI出了：", chinese[ai])

  # 输出对决结果
  # 除去相等的情况，用户输入的克星正好是AI出的就输了，否则就赢
  if user == ai:
    print("平局！")
  elif hands[user] == ai:
    print("你输了！")
  else:
    print("你赢了！")
    
else:
  print("请输入V、G或W！")
  

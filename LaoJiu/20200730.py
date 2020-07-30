'''
@Description: 
@Author: 陈十一
@Date: 2020-07-30 10:05:48
@LastEditTime: 2020-07-30 10:20:23
@LastEditors: 陈十一
'''
import math

n = int(input("请输入店数："))
time = 0

for i in range(n):
  
  inputStr = input("请按行输入坐标和钻石数，以空格分割：")

  # 切割输入并转为数字
  inputNum = inputStr.split(" ")
  numbers = [int(_) for _ in inputNum]
  
  # 计算距离
  distance = pow(pow(numbers[0], 2) + pow(numbers[1], 2), 0.5)
  
  # 取钻石数
  diamonds = numbers[2]

  # 计算时间
  time =  time + distance * 2 / 50 + diamonds * 1.5

# 向上取整后输出
print(math.ceil(time))
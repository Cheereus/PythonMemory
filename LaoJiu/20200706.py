'''
@Description: 
@Author: 陈十一
@Date: 2020-07-06 10:02:16
@LastEditTime: 2020-07-06 10:06:41
@LastEditors: 陈十一
'''

print("请输入十个整数")
price = [235, 206, 267, 2697, 270, 499, 171, 804, 108, 108]
sum = 0

for i in range(10):
  number = int(input())
  sum = sum + price[i] * number

print("总计需要：", sum, "积分！")
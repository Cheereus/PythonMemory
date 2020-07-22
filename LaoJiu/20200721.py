'''
@Description: 
@Author: 陈十一
@Date: 2020-07-21 10:14:13
@LastEditTime: 2020-07-21 10:23:19
@LastEditors: 陈十一
'''

print('请输入n:')
n = int(input())

output = 0

# 遍历求和
for i in range(1, n + 1):
  item = (i + 1) / i
  output = output + item

print(round(output, 4))
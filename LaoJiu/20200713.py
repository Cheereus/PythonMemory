'''
@Description: 
@Author: 陈十一
@Date: 2020-07-10 09:54:42
@LastEditTime: 2020-07-13 10:32:20
@LastEditors: 陈十一
'''

print("请输入1-26之间的数字：")

# 生成所有大写字母
characters = [chr(i) for i in range(65,91)]

# 储存输入
number = int(input())

# 储存输入
output = ''

# 长度为1的时候特殊处理一下
if number == 1:
  print("A")

elif number > 1 and number <= 26:
  
  # 遍历加起来
  for i in range(0, number - 1):
    output = output + "A" + characters[i + 1]

  # 将原字符串倒序再加到自身，去除中间重复的一个字符
  output = output[0:len(output)-1] + output[::-1]
  print(output)
else:
  print("输入数字不正确！")
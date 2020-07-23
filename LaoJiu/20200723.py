'''
@Description: 
@Author: 陈十一
@Date: 2020-07-23 09:47:50
@LastEditTime: 2020-07-23 10:16:31
@LastEditors: 陈十一
'''
print("请输入m:")
m = int(input())

# 数学推导可得奇数范围，然后生成对应列表
nums = [i for i in range(m * m - m + 1, m * m + m + 1, 2)]

# 平平无奇的字符串拼接
output = str(m) + "*" + str(m) + "*" + str(m) + "\n=" + str(m*m*m) + "\n="
for i in nums:
  output = output + str(i) + "+"

# 删除最后多余的加号后输出
print(output[:-1])  
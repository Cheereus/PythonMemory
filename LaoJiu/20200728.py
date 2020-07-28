'''
@Description: 
@Author: 陈十一
@Date: 2020-07-28 10:08:10
@LastEditTime: 2020-07-28 10:10:11
@LastEditors: 陈十一
'''

n = int(input("请输入直线条数："))

# 直接通项公式干！
p = int(n * (n + 1) / 2 + 1)

print("最多可将圆分为", p, "部分")

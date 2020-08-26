'''
Description: 
Author: CheeReus_11
Date: 2020-08-26 10:01:56
LastEditTime: 2020-08-26 10:30:49
LastEditors: CheeReus_11
'''

a = int(input('请输入a:'))
b = int(input('请输入b:'))
c = int(input('请输入c:'))

x = 2
min_x = False

# 除数不能比被除数还大
while x <= a and x <= b and x <= c:

    # 全写在判断条件里有点乱, 分开写
    res_a = a % x
    res_b = b % x
    res_c = c % x
    if (res_a == res_b) and (res_b == res_c):
        print('余数为:', res_a)
        min_x = True
        break
    x += 1

# 输出
if min_x:
    print('满足条件的 x 为:', x)
else:
    print(min_x)
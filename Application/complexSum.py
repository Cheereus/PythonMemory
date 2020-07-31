'''
@Description: 
@Author: 陈十一
@Date: 2020-07-31 16:56:44
@LastEditTime: 2020-07-31 17:46:52
@LastEditors: 陈十一
'''
import matplotlib.pyplot  as plt
from scipy.special import zeta
from mpmath import *
import numpy as np
from sympy import *
import math
init_printing()

# 设置 y 的取值间隔
step = 1

# 初始值
t = 1
# 区间长度
length = 1


n = Symbol('n', integer=True)
a=1
b=1
c = complex(a, b)
d = complex(0, -1)
k = [i for i in np.arange(t, t + length, step)]


expr = [complex(Sum(abs(1-c*n**d)/ n**(1+1/i), (n,1, oo)).evalf()).real for i in k]
print(expr[0])
# SumArr = [Sum(i, (n,1, oo)).evalf() for i in expr]
# print(SumArr)
#Sum(expr, (n, 1, oo)), Sum(expr, (n, 1, oo)).doit()
plt.scatter(k, expr)
plt.show()
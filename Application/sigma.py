'''
@Description: 
@Author: 陈十一
@Date: 2020-07-30 17:08:29
@LastEditTime: 2020-07-30 18:38:37
@LastEditors: 陈十一
'''

import matplotlib.pyplot  as plt
from scipy.special import zeta
import numpy as np

# 设置 y 的取值间隔
step = 0.1

# 初始值
t = 0.0
# 区间长度
length = 1000

# 生成点坐标并画散点图
Y = [i for i in np.arange(t, t + length, step)]
Value = [i * zeta(i + 1, 1) for i in Y]

plt.scatter(Y, Value, alpha=0.6, s=1)
plt.show()

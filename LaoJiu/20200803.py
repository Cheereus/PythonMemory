'''
Description: 
Author: 陈十一
Date: 2020-08-03 11:03:32
LastEditTime: 2020-08-03 11:24:49
LastEditors: 陈十一
'''
import math

# 输入数据
M = int(input("M:"))
N = int(input("N:"))
X = int(input("X:"))

# 当前体力值，初始为 0
C = 0

# 计数器
t = 1

# 士力架能够将体力值加满才能继续战斗
while X >= M - C:

  # 计算需要消耗的士力架
  eat = math.ceil((M - C) / N)

  print("第", t, "次战斗:")
  print("初始体力：", C, "战斗力：", N, "需要", eat, "根士力架补充, 战斗期", M, "天")
  # 每次战斗的流程
  # 补充体力并消耗士力架
  X = X - eat
  C = M

  # 增加战力
  N = N + M // N
  # 消耗体力
  C = C - M

  # 计数
  t = t + 1

  print("第", M, "天结束时战斗力为: ", N, "士力架剩余", X)
  print("-----------")

print("第", t, "次战斗:")
print("初始体力：", C, "战斗力：", N, "需要", math.ceil((M - C) / N), "根士力架补充, 战斗期", M, "天, 无法提升战斗力")
print("-----------")
print("最终战力：", N)


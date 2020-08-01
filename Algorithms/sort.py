'''
@Description: 排序算法实践，均为升序
@Author: 陈十一
@Date: 2020-08-01 09:14:26
@LastEditTime: 2020-08-01 10:57:53
@LastEditors: 陈十一
'''

import random

data = [random.randint(0,100) for _ in range(10)]

print(data)

# 选择排序
def Selection(a=[]):
  N = len(a)

  for i in range(N):
    min = i
    for j in range(i + 1, N):
      if a[j] < a[min]:
        min = j
    a[i], a[min] = a[min], a[i]

  print(a)
  return a

# 插入排序
def Insertion(a=[]):
  N = len(a)

  for i in range(N):
    j = i
    while j > 0 and a[j] < a[j - 1]:
      a[j], a[j - 1] = a[j - 1], a[j]
      j = j - 1 
      
  print(a)
  return a

# 对于随机排序的无重复主键数组，插入排序和选择排序的运行时间是平方级别的，两者之比是一个较小的常数
# Selection(data)
# Insertion(data)

# 希尔排序
def Shell(a=[]):
  N = len(a)
  
  h = 1
  while h < N // 3:
    h = 3 * h + 1

  while h >= 1:
    for i in range(h, N):
      j = i

      while j >= h and a[j] < a[j - 1]:
        a[j], a[j - 1] = a[j - 1], a[j]
        j = j - h  

    # 此处一定要整除，否则第二次循环时 h 就变成 float 了
    h = h // 3
  
  print(a)
  return a

# Shell(data)

# 原地归并排序 TODO 有 bug

def merge(a=[], lo=0, mid=0, hi=0):
  i = lo
  j = mid + 1
  aux = [None] * len(a)
  
  k = lo
  while k <= hi:
    aux[k] = a[k]
    k = k + 1

  k = lo
  while k <= hi:
    if i > mid:
      a[k] = aux[j]
      j = j + 1
    elif j > hi:
      a[k] = aux[i]
      i = i + 1
    elif aux[j] < aux[i]:
      a[k] = aux[j]
      j = j + 1
    else:
      a[k] = aux[i]
      i = i + 1
    k = k + 1
  
  return a

# 自顶向下的归并排序
def Merge(a):

  aux = [None] * len(a)
  
  def sort(b, lo, hi):
    if hi <= lo:
      return
    mid = lo + (hi - lo) // 2
    sort(b, lo, mid)
    sort(b, mid + 1, hi)
    merge(b, lo, mid, hi)
  
  sort(a, 0, len(a) - 1)

# 对于长度为 N 的任意数组，自顶向下的归并排序需要 1/2NlgN 至 NlgN 次比较
Merge(data)

print(data)

      

'''
Description: 
Author: CheeReus_11
Date: 2020-09-02 14:13:40
LastEditTime: 2020-09-02 16:12:32
LastEditors: CheeReus_11
'''

# 两个有序数组中寻找中位数
# 遍历两个数组综合排序前一半的数字
def find_mid(A=[], B=[]):
    la = len(A)
    lb = len(B)
    i = 0
    j = 0
    mid = 0
    # 如果A和B等长, 可以加个极端条件判断
    # if A[la - 1] < B[i]:
    #     mid = B[i]
    # elif B[lb - 1] < A[i]:
    #     mid = A[i]
    # else:
    while i + j < (la + lb) / 2:
        # 交替遍历两个数组, 遍历一半即止
        if A[i] <= B[j]:
            mid = A[i]
            i += 1
        else:
            mid = B[j]
            j += 1

    return mid
  
print(find_mid([1,2,3,4,4,6], [1,2,4,4,5,6]))

# 应该还可以用折半查找, 先交一版
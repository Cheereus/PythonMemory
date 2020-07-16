'''
@Description: 
@Author: 陈十一
@Date: 2020-07-16 10:16:02
@LastEditTime: 2020-07-16 14:27:28
@LastEditors: 陈十一
'''

print("请输入忘了提交的天数：")
# 忘提交的天数
num_days_missed = int(input())

print("请输入补签卡数量：")
# 补签卡数量
num_cards = int(input())

# 卡比天数多还有啥好算的呢？
if num_cards >= num_days_missed:
  print("100天！这还用算？")

else:
  # 未签日期
  days = []
  print("请输入未签到的日期")
  for _ in range(num_days_missed):
    days.append(int(input()))
  # 给输入排序
  days.sort()
  # 根据日期计算被分割的连续天数, 被断签的 n 天分割为了 n+1 个连续天数
  continue_days = []
  # 第一个连续天数即为第一个断签日减一
  continue_days.append(days[0] - 1)
  # 中间的连续天数即为两个断签日相减再减一
  for i in range(num_days_missed - 1):
    continue_days.append(days[i+1] - days[i] - 1)
  # 最后一个连续天数即为 100 减去最后一天
  continue_days.append(100 - days[num_days_missed - 1])

  days_after = 0
  if num_cards == 0:
    days_after = continue_days[0]
    print(days_after, "天，没卡就别来算了！")
    
  # 按补签卡数量，寻找连续天数序列中的最大子数组
  else:
    for i in range(0, num_days_missed - num_cards + 1):
      # 要记得加上补签的那几天
      sum_days = sum(continue_days[i:(i + num_cards + 1)]) + num_cards
      print(continue_days[i:(i + num_cards + 1)], ':' ,sum_days)
      if sum_days > days_after:
        days_after = sum_days
    
  print("补签后最大连续天数为：", days_after)

    
  
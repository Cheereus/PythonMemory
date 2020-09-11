'''
Description: 调用高德地图逆地理编码API 根据经纬度查询街道信息
Author: 陈十一
Date: 2020-08-03 14:23:35
LastEditTime: 2020-08-12 14:59:00
LastEditors: CheeReus_11
'''
import requests
import xlrd
import openpyxl
import pandas as pd
import math

# 高德逆地理编码 API https://lbs.amap.com/api/webservice/guide/api/georegeo
# 请求参数
baseUrl = 'https://restapi.amap.com/v3/geocode/regeo'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

# key 为高德开放平台应用生成的密钥
# location 为经度与维度通过逗号相连的字符串
params = {"location" : "", "key" : "0a3497aef8cfbce51cfb734df4ff5396"}

# 文件路径
filePath = 'data/2.xlsx'
x1 = xlrd.open_workbook(filePath)

# 获取经纬度 list
sheet = x1.sheets()
longitudes = sheet[0].col_values(1)
latitude = sheet[0].col_values(2)

rows = len(longitudes)

businessAreas = []
streets = []
township = []

# 记录异常返回的数据
errors = []

# 如果使用百度的经纬度，则需要先转化为高德经纬度
# 百度经纬度转高德
def baiduToGaode(lng, lat):
  x_pi = 3.14159265358979324 * 3000.0 / 180.0;
  x = lng - 0.0065;
  y = lat - 0.006;
  z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi);
  theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi);
  lngs = z * math.cos(theta);
  lats = z * math.sin(theta);

  return round(lngs, 6), round(lats, 6)   

# 请求高德地图 API
def getData(xb, yb):
  x, y = baiduToGaode(xb, yb)
  print(x, y)
  params["location"] = str(x) + "," + str(y)
  response = requests.get(url=baseUrl, params=params, headers=headers)
  return response.json()

# print(getData(116.3646, 40.07209))

# 生成街道信息 list
for i in range(0, rows):
  try:
    print(i, "of", rows)
    data = getData(longitudes[i], latitude[i])
    tmp = data.get('regeocode').get('addressComponent').get('township')
    
    # 高德对于查询不到的 township, 会返回一个空数组, 需要将其处理为空字符串否则无法写入 excel 文件
    if type(tmp) == type([]):
      errors.append(i)
      tmp = ''
      
    township.append(tmp)
  except ValueError:
    print(ValueError, i)

# 存储数据
wb = openpyxl.load_workbook(filePath)
ws = wb.worksheets[0]
ws.insert_cols(4)

for index, row in enumerate(ws.rows): #按行读取
    # if index == 0:
    #   row[3].value = '街道'
    # else:
    if index < len(township):
      print(index, "of", rows)
      row[3].value = township[index]

# 输出异常数据的索引并保存所有数据到文件
print("异常数据", errors)
wb.save('data/0_new.xlsx')
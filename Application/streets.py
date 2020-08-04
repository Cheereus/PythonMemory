'''
Description: 调用高德地图逆地理编码API 根据经纬度查询街道信息
Author: 陈十一
Date: 2020-08-03 14:23:35
LastEditTime: 2020-08-04 14:45:03
LastEditors: 陈十一
'''
import requests
import xlrd
import openpyxl

# 请求参数
baseUrl = 'https://restapi.amap.com/v3/geocode/regeo'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
params = {"location" : "", "key" : "0a3497aef8cfbce51cfb734df4ff5396"}

# 文件路径
filePath = 'data/石景山小区经纬度.xlsx'

x1 = xlrd.open_workbook(filePath)
sheet = x1.sheets()

longitudes = sheet[0].col_values(1)
latitude = sheet[0].col_values(2)

rows = len(longitudes)

businessAreas = ["businessAreas"]
streets = ["streets"]
township = ["township"]

# 请求高德地图 API
def getData(x, y):
  params["location"] = str(x) + "," + str(y)
  response = requests.get(url=baseUrl, params=params, headers=headers)
  return response.json()

# 生成街道信息 list
for i in range(1, rows):
  try:
    data = getData(longitudes[i], latitude[i]);
    township.append(data.get('regeocode').get('addressComponent').get('township'))
  except ValueError:
    print(ValueError, i)
  print(i)

# 存储数据
wb = openpyxl.load_workbook(filePath)
ws = wb.worksheets[0]
ws.insert_cols(4)

for index, row in enumerate(ws.rows):#按行读取
    if index == 0:
        row[3].value = '街道'
    else:
        row[3].value = township[index]
wb.save('data/0_new.xlsx')

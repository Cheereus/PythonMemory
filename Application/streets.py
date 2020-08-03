'''
Description: 
Author: 陈十一
Date: 2020-08-03 14:23:35
LastEditTime: 2020-08-03 14:40:55
LastEditors: 陈十一
'''
import requests

baseUrl = 'https://restapi.amap.com/v3/geocode/regeo'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
params = {"location" : "", "key" : "0a3497aef8cfbce51cfb734df4ff5396"}

def getData(x, y):
  params["location"] = str(x) + "," + str(y)
  response = requests.get(url=baseUrl, params=params, headers=headers).text
  print(response)

getData(116.3384, 39.88922)

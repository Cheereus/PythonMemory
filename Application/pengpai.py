import requests

# 请求参数
baseUrl = 'https://www.thepaper.cn/'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
params = {"pageidx": 1}

response = requests.get(url=baseUrl, headers=headers)
print(response.content.decode('utf-8', 'ignore'))

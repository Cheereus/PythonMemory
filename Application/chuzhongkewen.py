# 一共六个列表页面 从 /Catalog/19/ 到 /Catalog/24/
# 列表页中 div.right ul li a 的 href 即为每篇文章地址
# 每篇文章中 div.file_content div.title 即为文章标题 div.txt 中的 p 即为文章内容


import urllib.request
from bs4 import BeautifulSoup
baseUrl = 'http://www.968816.com'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
catalogs = []
for n in range(19, 25):
    catalogs.append(baseUrl + '/Catalog/' + str(n) + '/')

def getArticle(title, href): # 获取文章内容
    req = urllib.request.Request(href, None, header)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html5lib')
    article = soup.find('div', 'file_content')
    content = article.find_all('p')
    txt = ''
    if len(content) == 0:
        title = '暂缺/' + title
        print(title)
    for p in content:
        txt += p.get_text()
    saveFile = open('E:/c/articles/' + title + '.txt', mode='w', encoding='utf-8')
    saveFile.write(txt)
    saveFile.close()


def getCatalogList(cat): # 获取文章列表
    req = urllib.request.Request(cat, None, header)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html5lib')
    links = soup.find('div', 'right').ul.find_all('a')
    hrefs = [];
    for link in links:
        hrefs.append(link.get('href'))
        getArticle(link.get_text().strip(), baseUrl + link.get('href'))

for cat in catalogs:
    print(cat)
    getCatalogList(cat)

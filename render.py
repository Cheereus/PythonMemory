import os
import shutil

print("此脚本用于dzf-agent项目。请预先准备好以下内容：\n分站英文名\n主站域名\n两个颜色值\n分站中文名\n代理商ID\nQQ号(可选)\n微信图片请手动替换\n----------")

nameEng = ''  

# 替换文件内容
def replaceAndSave(file_path, old_str, new_str):
    f = open(nameEng + "/" + file_path,'r+', encoding='UTF-8')
    all_lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in all_lines:
      line = line.replace(old_str, new_str)
      f.write(line)
    f.close()

# 输入分站英文名替换并据此生成文件夹
nameEng = input("请输入分站英文名称:")
shutil.copytree('tpl', nameEng)
replaceAndSave('index.html', '{nameEng}', nameEng)
replaceAndSave('resources/script/head.js', '{nameEng}', nameEng)
print('新建分站目录成功\n----------')

# 替换主域名
domainName = input("请输入主站域名:")
replaceAndSave('index.html', '{domainName}', domainName)
print('主站域名替换成功\n----------')

# 输入两个颜色用作渐变色，第二种颜色同时作为按钮和logo字体颜色
color1 = input("请输入颜色1:")
color2 = input("请输入颜色2:")
replaceAndSave('resources/css/style.css', '{color1}', color1)
replaceAndSave('resources/css/style.css', '{color2}', color2)
print("颜色替换成功\n----------")

# 输入分站中文名替换
nameZh = input("请输入中文名称:")
replaceAndSave('index.html', '{nameZh}', nameZh)
replaceAndSave('resources/script/head.js', '{nameZh}', nameZh)
print("中文名替换成功\n----------")

# 输入代理商ID
ugentId = input("请输入代理商ID:")
replaceAndSave('resources/script/head.js', '{ugentId}', ugentId)
print("代理商ID替换成功\n----------")

# 输入QQ(可选)替换
QQ = input("请输入QQ:")
replaceAndSave('resources/script/head.js', '{QQ}', QQ)
print("QQ替换成功\n----------")

print("脚本已执行完成，已生成对应目录，请手动替换微信图片以及进行其他操作\n")
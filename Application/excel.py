import xlrd
worksheet = xlrd.open_workbook('CNKI2.xls')
sheet_names = worksheet.sheet_names()
keywords = []
keywordTimes = {}
for sheet_name in sheet_names:
    sheet2 = worksheet.sheet_by_name(sheet_name)
    cols = sheet2.col_values(5) # 获取第四列内容
    for item in cols:
        cuts = item.split(';;')
        for cut in cuts:
            keywords.append(cut)
for keyword in keywords:
    if keyword in keywordTimes:
        keywordTimes[keyword] += 1
    else:
        keywordTimes[keyword] = 1
sorted_dict = sorted(keywordTimes.items(), key=lambda item: item[1], reverse=True)
for item in sorted_dict:
    print(item)
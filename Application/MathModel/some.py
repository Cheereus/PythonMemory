import xlrd
import joblib


def read_from_xlsx(filePath):
    f = xlrd.open_workbook(filePath)
    sheets = f.sheets()
    return sheets[0]


print('Reading excel file...')
data = read_from_xlsx('data/down_connection.xlsx')

print('Data processing...')
up_connection = []

row = data.nrows  # 总行数
for i in range(row):
    row_data = data.row_values(i)  # 第 i 行
    up_connection.append(row_data)

# 直接保存为二进制文件，避免再重复读取 excel
print('Saving...')
joblib.dump(up_connection, 'data/down_connection.pkl')
print(up_connection)

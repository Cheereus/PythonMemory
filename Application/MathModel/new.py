import xlrd
import joblib


def read_from_xlsx(filePath):
    f = xlrd.open_workbook(filePath)
    sheets = f.sheets()
    return sheets[0]


print('Reading excel file...')
data = read_from_xlsx('data/222222.xlsx')

print('Data processing...')
invoice_data = []
rate = []

row = data.nrows  # 总行数
for i in range(1, row):
    row_data = data.row_values(i)  # 第 i 行
    invoice_data.append(row_data[1:9])
    rate.append(row_data[9])
    print(row_data[9], '/', row - 1)

# 直接保存为二进制文件，避免再重复读取 excel
print('Saving...')
joblib.dump([invoice_data, rate], 'data/data_2.pkl')


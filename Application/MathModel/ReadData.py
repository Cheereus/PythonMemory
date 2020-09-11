import xlrd
import joblib

def read_from_xlsx(filePath):
    f = xlrd.open_workbook(filePath)
    sheets = f.sheets()
    return sheets

# 从 excel 中分别读取公司信息、进项发票、销项发票
print('Reading excel file...')
company_info, invoice_in, invoice_out = read_from_xlsx('data/302.xlsx')

# 企业代号列表
companies = company_info.col_values(0)[1:]
# 信用评级
# rate = company_info.col_values(2)[1:]

print('Data processing...')
# 按企业对发票信息进行遍历
def get_invoice_data(invoice_sheet, c):
    invoice_data = [[] for i in range(len(c))] 

    row = invoice_sheet.nrows #总行数
    for i in range(1, row):
        row_data =invoice_sheet.row_values(i)   # 第 i 行
        company_index = c.index(row_data[0])
        money = row_data[4]
        tax = row_data[5]
        status = 1 if row_data[7] == '有效发票' else 0
        invoice_data[company_index] += [[money, tax, status]]
        print(i, '/', row - 1)

    return invoice_data

invoice_in_data = get_invoice_data(invoice_in, companies)
invoice_out_data = get_invoice_data(invoice_out, companies)
data = [companies, invoice_in_data, invoice_out_data]

# 直接保存为二进制文件，避免再重复读取 excel
print('Saving...')
joblib.dump(data, 'data/data_predict.pkl')








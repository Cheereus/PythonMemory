import xlrd
import joblib


def read_from_xlsx(filePath):
    f = xlrd.open_workbook(filePath)
    sheets = f.sheets()
    return sheets


print('Loading data...')
companies, rate, invoice_in_data, invoice_out_data = joblib.load('data/data_train.pkl')
day_money = read_from_xlsx('data/day_money.xlsx')[0].row_values(0)

# 对于每个公司，计算进项销项发票金额总和，税额总和，发票比数，发票作废率
data_after_process = []

for i in range(len(companies)):

    # 第 i 个公司的发票
    invoice_in = invoice_in_data[i]
    invoice_out = invoice_out_data[i]
    print(len(invoice_in))
    print(len(invoice_out))

    # 进项和
    sum_in_money = 0
    sum_in_tax = 0
    invalid_in = 0

    for invoice in invoice_in:
        if invoice[2] == 0:
            invalid_in += 1
        else:
            sum_in_money += float(invoice[0])
            sum_in_tax += float(invoice[1])

    # 销项和
    sum_out_money = 0
    sum_out_tax = 0
    invalid_out = 0

    for invoice in invoice_out:
        if invoice[2] == 0:
            invalid_out += 1
        else:
            sum_out_money += float(invoice[0])
            sum_out_tax += float(invoice[1])

    # 合成数据向量
    data_after_process.append([(sum_out_money + sum_out_tax - sum_in_money - sum_in_tax) / (
                sum_out_money + sum_out_tax + sum_in_money + sum_in_tax), invalid_out / len(invoice_out),
                               len(invoice_in) + len(invoice_out), day_money[i]])

print(data_after_process[-1])

# 直接保存为二进制文件
print('Saving...')
joblib.dump([companies, rate, data_after_process], 'data/data_train_after.pkl')

output = open('QC_ALL.txt', 'w', encoding='utf-8')
Chr = list(range(1, 19)) + ['X', 'Y']
for c in Chr:
    input_file = open('QC_Result/Chr' + str(c) + '.txt', encoding='utf-8')
    input_list = input_file.readlines()
    for input_line in input_list:
        output.writelines(input_line)
output.close()

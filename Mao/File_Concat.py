output = open('Chr_ALL.txt', 'w', encoding='utf-8')
for c in range(1, 19):
    input_file = open('find_result/Chr_chr' + str(c) + '.txt', encoding='utf-8')
    input_list = input_file.readlines()
    for input_line in input_list:
        output.writelines(input_line)
output.close()

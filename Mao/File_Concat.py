output = open('result/Chr_ALL.txt', 'w')
for c in range(1, 19):
    input_file = open('result/Chr_' + str(c) + '.txt', encoding='utf-8')
    input_list = input_file.readlines()
    for input_line in input_list:
        output.writelines(input_line)
output.close()

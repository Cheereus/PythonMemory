import numpy as np

# Read data from `.txt` file
def read_from_txt(filePath):
    f = open(filePath)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(str,line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    array_data = np.array(data_list)
    return array_data

data = read_from_txt('./DD-SCORE.txt')

print(data.shape)
# 按第四列排序
data = data[data[:, 3].astype('int64').argsort()]

# 窗口大小
window_size = 8500000

f = open('./chip_DD_300.txt','a')

for i in range(1,19):

    # 当前最大值和最大行
    tmp_max = 0
    max_line = []
    
    # 窗口索引
    group = 1
    
    # 遍历每一行
    for line in data:
        
        chromosome = int(line[0])
        location = int(line[3])
        value = float(line[2])

        if chromosome == i:
            
            # 在每进入下一个窗口的时候，将前一个窗口的最大值写入文件
            if location >= group * window_size:
                print(chromosome)
                if tmp_max != 0:
                    f.writelines(' '.join(max_line) + '\n')
                group += 1
                tmp_max = 0
            if value > tmp_max:
                # 更新最大值和最大行
                tmp_max = value
                max_line = line
    f.writelines(' '.join(max_line) + '\n')
f.close()

input_str = '70000 8 14'
input_str = input_str.split(' ')
N, x, y = [int(i) for i in input_str]

data = 0
ni = N
failed = False
i = 1
while i <= y:
    ni = ni * 2 / 3
    if i == x:
        ni += N / 2
    if ni < N / 32:
        failed = True
        break
    i += 1

output_str = str(format(ni, '.6f'))
a, b = output_str.split('.')
if len(b) < 6:
    b += '0' * (6 - len(b))
output_str = a + '.' + b

if failed:
    print('N0!\n' + str(i), output_str)
else:
    print('YE5!\n' + str(output_str))

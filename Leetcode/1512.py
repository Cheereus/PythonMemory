nums = [1,2,3]

num_dict = {}

for n in nums:
    if n in num_dict:
        num_dict[n] += 1
    else:
        num_dict[n] = 1

print(num_dict)
sums = 0
for key in num_dict.keys():
    sums += (num_dict[key] * (num_dict[key] - 1)) / 2

print(sums)

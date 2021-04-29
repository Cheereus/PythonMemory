from Utils import get_color, draw_scatter, read_from_txt

data = read_from_txt('pca.txt', head=True)

# print(data)

default_colors = [[138/256, 158/256, 202/256], [246/256, 140/256, 99/256], [98/256, 194/256, 164/256]]

label_dict = {'DD': 'Duroc', 'LL': 'Landrace', 'YY': 'Yorkshire'}

labels = data[:, 0]
labels = [label_dict[i] for i in labels]
x = data[:, 2]
y = data[:, 3]
x = [float(i) for i in x]
y = [float(i) for i in y]
print(x)
print(y)
colors = get_color(labels, default_colors)
print(len(colors))

draw_scatter(x, y, labels, colors, xlabel='PC1(56.84%)', ylabel='PC2(35.73%)')

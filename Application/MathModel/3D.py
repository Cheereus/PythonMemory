import joblib
from Utils import get_color, draw_scatter3d

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')

# get three coordinates
x = [i[0] for i in data_after_process]
y = [i[1] for i in data_after_process]
z = [i[2] for i in data_after_process]
colors = get_color(rate, colors=None)

z_max = max(z)

draw_scatter3d(x, y, [i / z_max for i in z], rate, colors=colors)

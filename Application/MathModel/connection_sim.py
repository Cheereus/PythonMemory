import joblib
from sklearn.model_selection import LeaveOneOut
from Utils import get_color
import numpy as np
from Clustering import knn

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')
up_connection = np.array(joblib.load('data/up_connection.pkl'))
down_connection = np.array(joblib.load('data/down_connection.pkl'))

connection = up_connection + down_connection

labels_int = np.array(get_color(rate, [1, 2, 3, 4]))

loo = LeaveOneOut()
correct = 0
for train, test in loo.split(connection):
    model = knn(connection[train], labels_int[train], 3)
    labels_predict = model.predict(connection[test])
    if labels_predict == labels_int[test]:
        correct += 1
print(correct / len(rate))

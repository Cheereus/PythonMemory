import numpy as np
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

np.random.seed(1)
X = np.load('X.npy')
Y = np.load('Y.npy')
data_size = X.shape[0]
X = X.reshape((data_size, 224*224))
#
data_size = len(Y)
index_list = list(range(data_size))
np.random.shuffle(index_list)
X = X[index_list]
Y = Y[index_list]

test_rate = 0.1
train_index = int(data_size*(1-test_rate))
train_data = X[:train_index]
train_Y = Y[:train_index]
test_data = X[train_index:]
test_Y = Y[train_index:]

Positive_data = []
Negative_data = []

for i in range(len(train_data)):
    if train_Y[i] == 1:
        Positive_data.append(train_data[i])
    else:
        Negative_data.append(train_data[i])
        Negative_data.append(train_data[i])
        Negative_data.append(train_data[i])

print(len(Positive_data), len(Negative_data))

train_data = np.array(Positive_data + Negative_data)
train_Y = np.array([1]*len(Positive_data) + [0]*len(Negative_data))
data_size = len(train_data)
index_list = list(range(data_size))
np.random.shuffle(index_list)
train_data = train_data[index_list]
train_Y = train_Y[index_list]

model = SVC(C=1, class_weight='balanced', kernel='linear')
# model = KNeighborsClassifier(n_neighbors=5)
model.fit(train_data, train_Y)

predict_Y = model.predict(test_data)
acc = accuracy_score(predict_Y, test_Y)
recall = recall_score(predict_Y, test_Y)
precision = precision_score(predict_Y, test_Y)

print('True label ', test_Y)
print('Pred label ', predict_Y)
print('Accuracy   ', acc)
print('Recall     ', recall)
print('precision  ', precision)

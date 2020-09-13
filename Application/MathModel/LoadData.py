import joblib
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from Utils import get_color, draw_scatter
from Clustering import k_means, knn
from Metrics import ARI, accuracy, NMI, F1
from sklearn.model_selection import cross_val_score, LeaveOneOut
import numpy as np

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')
up_connection = joblib.load('data/down_connection.pkl')


# SVM with best params using gridsearch and cross validation
def svm_grid_search(x, y, s=10):
    svc = svm.SVC()
    parameters = [
        {
            'C': [1, 3, 5],
            'gamma': [0.001, 0.1, 1, 10],
            'degree': [3, 5, 7, 9],
            'kernel': ['rbf', 'sigmoid'],
            'decision_function_shape': ['ovo', 'ovr', None]
        }
    ]
    clf = GridSearchCV(svc, parameters, cv=s, refit=True)
    clf.fit(x, y)

    return clf.best_estimator_, clf.best_params_


def svm_cross_validation(x, y, params, s=10):
    cross_model = svm.SVC(C=params['C'], degree=params['degree'], kernel=params['kernel'], gamma=params['gamma'],
                          decision_function_shape=params['decision_function_shape'], verbose=0)
    scores = cross_val_score(cross_model, x, y.ravel(), cv=s)
    return scores


def svm_predict(x, model):
    results = model.predict(x)
    return results


labels_int = get_color(rate, [1, 2, 3, 4])

# knn training and predict
# model = knn(up_connection, labels_int, 3)
# labels_predict = model.predict(up_connection)

up_connection = np.array(up_connection)
labels_int = np.array(labels_int)

loo = LeaveOneOut()
correct = 0
for train, test in loo.split(up_connection):
    model = knn(up_connection[train], labels_int[train], 3)
    labels_predict = model.predict(up_connection[test])
    if labels_predict == labels_int[test]:
        correct += 1
print(correct / len(rate))


# draw_scatter(x, y, labels_predict, labels_int)

# print(scores)

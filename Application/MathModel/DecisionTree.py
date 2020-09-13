from sklearn import tree
from sklearn.model_selection import cross_val_score, LeaveOneOut
import joblib
import graphviz
import pydotplus
import numpy as np

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')

data_after_process = np.array(data_after_process)
rate = np.array(rate)

clf = tree.DecisionTreeClassifier(max_depth=10)

# scores = cross_val_score(clf, data_after_process, rate, cv=10)
# print(scores)
loo = LeaveOneOut()
correct = 0
for train, test in loo.split(data_after_process):
    print(train, test)
    clf.fit(data_after_process[train], rate[train])  # fitting
    y_p = clf.predict(data_after_process[test])
    if y_p == rate[test]:
        correct += 1
print(correct / len(rate))

clf = clf.fit(data_after_process, rate)

joblib.dump(clf, 'data/model.pkl')

print(rate)

dot_data = tree.export_graphviz(clf, out_file=None,
                                #               利润率     作废率      发票比数    平均每日交易额
                                feature_names=['profit', 'invalid', 'numbers', 'day_money'],
                                class_names=['A', 'B', 'C', 'D'],
                                filled=True, rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("result.pdf")

''''''

from sklearn import tree
from sklearn.model_selection import cross_val_score, LeaveOneOut
import joblib
import graphviz
import pydotplus
from Metrics import ARI, accuracy, NMI, F1
import openpyxl

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_train_after.pkl')

clf = tree.DecisionTreeClassifier(max_depth=None)

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

dot_data = tree.export_graphviz(clf, out_file=None,
                                #
                                feature_names=['profit', 'avg_in', 'avg_out'],
                                class_names=rate,
                                filled=True, rounded=True,
                                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("result.pdf")

''''''

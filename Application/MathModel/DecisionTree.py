from sklearn import tree
from sklearn.model_selection import cross_val_score
import joblib 
import graphviz
import pydotplus 

print('Loading data...')
companies, rate, data_after_process = joblib.load('data/data_after_process.pkl')

clf = tree.DecisionTreeClassifier(max_depth=5)

cross_model = clf
scores = cross_val_score(cross_model, data_after_process, rate, cv=10)
print(scores)

clf = clf.fit(data_after_process, rate)

dot_data = tree.export_graphviz(clf, out_file=None, 
                                         # 进项金额总和，     进项税额总和，   进项作废率，    进项发票比数，      销项金额总和，      销项税额总和，    销项作废率，     销项发票比数
                         feature_names = ['sum_in_money', 'sum_in_tax', 'invalid_in', 'num_invoice_in', 'sum_out_money', 'sum_out_tax', 'invalid_out', 'num_invoice_out'],  
                         class_names = rate,  
                         filled = True, rounded=True,  
                         special_characters = True) 
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("result.pdf")
from sklearn import tree
from sklearn.model_selection import cross_val_score
import joblib
import graphviz
import pydotplus
from Metrics import ARI, accuracy, NMI, F1
import openpyxl

print('Loading data...')
companies, data_after_process = joblib.load('data/data_predict_after_process.pkl')

print('Loading model...')
clf = joblib.load('data/model.pkl')

# clf = clf.fit(data_after_process, rate)

print('Predicting...')
labels_predict=clf.predict(data_after_process)
print(labels_predict)

print('Saving...')
# 存储数据
wb = openpyxl.load_workbook('data/302.xlsx')
ws = wb.worksheets[0]
ws.insert_cols(2)

for index, row in enumerate(ws.rows): #按行读取
    if index == 0:
        row[1].value = '预测评级'
    else:
        print(index)
        if index <= len(labels_predict):
        # print(index, "of", len(labels_predict))
            row[1].value = labels_predict[index - 1]

wb.save('data/0_new.xlsx')

# joblib.dump(clf, 'data/model.pkl')

# print('Accuracy:', accuracy(labels_predict, rate))

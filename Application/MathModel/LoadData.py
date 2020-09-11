import joblib

print('Loading data...')
companies, data_after_process = joblib.load('data/data_predict_after_process.pkl')

for i in range(17):

    print(companies[i], data_after_process[i])
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from Preprocess import train_data_filter
from sklearn.metrics import mean_squared_error
import sys

train_df = pd.read_csv('train.csv')

train_data = train_data_filter(train_df)

# Splitting the dataset into 2 set
x = train_data.drop('SalePrice', 1)
y = train_data['SalePrice']
print(x.shape, y.shape)
X_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

print(y_train.shape, X_train.shape)

model_ridge = Ridge()
model_ridge.fit(X_train, y_train)
predict_ridge = model_ridge.predict(x_test)

loss = mean_squared_error(y_test, predict_ridge, squared=False)
sys.stdout.write(str(loss))

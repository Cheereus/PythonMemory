import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from Preprocess import train_data_filter
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import sys

train_df = pd.read_csv('train.csv')
train_data = train_data_filter(train_df)
pca = PCA(n_components=6)
pca_data = pca.fit_transform(train_data.drop('SalePrice', 1))
# print(pca_data, pca_data.shape)
# Splitting the dataset into 2 set
x = pca_data
y = train_data['SalePrice']
# print(x.shape, y.shape)
X_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

# print(y_train.shape, X_train.shape)


model_pcalinear = LinearRegression()
model_pcalinear.fit(X_train, y_train)
predict_pcalinear = model_pcalinear.predict(x_test)

loss = mean_squared_error(y_test, predict_pcalinear, squared=False)
sys.stdout.write(str(loss))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error

test_df = pd.read_csv('test.csv')
train_df = pd.read_csv('train.csv')
# print(train_df.shape)
# print(train_df.isnull().sum())
# print(train_df.describe())
# print(train_df.info())
# print(train_df['SalePrice'].describe(percentiles=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1]))
# Generate and visualize the correlation matrix
corr = train_df.corr().round(2)

# Mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set figure size
f, ax = plt.subplots(figsize=(20, 20))

# Define custom colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

plt.tight_layout()
# plt.show()


# Dropping the less important columns
cols = ['MSZoning', 'Street',
        'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig',
        'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType',
        'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType',
        'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual',
        'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating',
        'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual', 'Functional', 'FireplaceQu', 'GarageType',
        'GarageFinish', 'GarageQual', 'GarageCond', 'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature', 'SaleType',
        'SaleCondition']

train_df = train_df.drop(cols, axis=1)

# Visualization with Important feature of dataset
# Generate and visualize the correlation matrix
corr = train_df.corr().round(2)

# Mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set figure size
f, ax = plt.subplots(figsize=(20, 20))

# Define custom colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

plt.tight_layout()
# plt.show()

train_df.LotFrontage.fillna(train_df.LotFrontage.mean(), inplace=True)
train_df.fillna(train_df.mean(), inplace=True)

# Splitting the dataset into 2 set
x = train_df.drop('SalePrice', 1)
y = train_df['SalePrice']
print(x.shape, y.shape)
X_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
model_logistic = LogisticRegression()
model_linear = LinearRegression()
model_ridge = Ridge()
model_ElasticNet = ElasticNet()

print(y_train.shape, X_train.shape)

model_logistic.fit(X_train, y_train)
model_linear.fit(X_train, y_train)
model_ridge.fit(X_train, y_train)
model_ElasticNet.fit(X_train, y_train)

predict_logistic = model_logistic.predict(x_test)
predict_linear = model_linear.predict(x_test)
predict_ridge = model_ridge.predict(x_test)
predict_ElastcNet = model_ElasticNet.predict(x_test)
# print(predict[1:6])
# prediction_logistic=model_logistic.predict_log_proba(x_test)
# print(prediction[1:6])


cols = ['MSZoning', 'Street',
        'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig',
        'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType',
        'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType',
        'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual',
        'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating',
        'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual', 'Functional', 'FireplaceQu', 'GarageType',
        'GarageFinish', 'GarageQual', 'GarageCond', 'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature', 'SaleType',
        'SaleCondition']

test_df = test_df.drop(cols, axis=1)
test_df.fillna(test_df.mean(), inplace=True)
prediction_logistic = model_logistic.predict(test_df)
prediction_linear = model_linear.predict(test_df)
prediction_ridge = model_ridge.predict(test_df)
prediction_ElastcNet = model_ElasticNet.predict(test_df)
print(prediction_logistic)
print(prediction_linear)
print(prediction_ridge)
print(prediction_ElastcNet)
# mean_squared_error()
my_submission_logistic = pd.DataFrame({'id': test_df.Id, 'SalePrice': prediction_linear})
my_submission_linear = pd.DataFrame({'id': test_df.Id, 'SalePrice': prediction_linear})
my_submission_ridge = pd.DataFrame({'id': test_df.Id, 'SalePrice': prediction_linear})
my_submission_ElastcNet = pd.DataFrame({'id': test_df.Id, 'SalePrice': prediction_linear})
my_submission_logistic.to_csv('submissionn_logistic.csv', index=False)
my_submission_linear.to_csv('submissionn_linear.csv', index=False)
my_submission_ridge.to_csv('submissionn_ridge.csv', index=False)
my_submission_ElastcNet.to_csv('submissionn_ElastcNet.csv', index=False)

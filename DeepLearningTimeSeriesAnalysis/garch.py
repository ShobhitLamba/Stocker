# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error

# Importing the training set
dataset_train = pd.read_csv('Datasets/Archived/MSFT_train.csv')
training_set = dataset_train.iloc[:, 4:5].values

X_train = np.array(training_set)
y_train = []

for i in range(1, 4284):
    y_train.append(X_train[i] - X_train[i-1])

X_train = X_train[1:]  
X_train_logtransformed = np.log(X_train)

n_test = 100
train, test = X_train_logtransformed[:-n_test], X_train_logtransformed[-n_test:]

# GARCH model
from arch import arch_model

model = arch_model(X_train_logtransformed, mean='Zero', vol='GARCH', p=15, q=15)

model_fit = model.fit()

# Testing on test data
dataset_test = pd.read_csv('Datasets/Archived/MSFT_test.csv')
real_stock_price = dataset_test.iloc[:, 4:5].values

yhat = model_fit.forecast(horizon=n_test)

# plot the actual variance
var = [i*0.1 for i in range(0,100)]
plt.plot(var[-n_test:])
# plot forecast variance
plt.plot(yhat.variance.values[-1, :])
plt.show()
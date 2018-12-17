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

# ARIMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(X_train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
#model = ARIMA(X_train, order=(5,1,0))
model_fit = model.fit(disp=False)
print(model_fit.summary())

residuals = pd.DataFrame(model_fit.resid)
plt.plot(X_train_logtransformed, label = 'Log Transformed')
plt.plot(residuals, color = 'red', label = 'Residuals') 
plt.show()
residuals.plot(kind='kde')
plt.show()
print(residuals.describe())

# Test on 2018 data
dataset_test = pd.read_csv('Datasets/Archived/MSFT_test.csv')
real_stock_price = dataset_test.iloc[:, 4:5].values
#real_stock_price = np.log(real_stock_price)

#predictions_ARIMA_diff = pd.Series(model_fit.fittedvalues, copy=True)
#
#predicted = predictions_ARIMA_diff[:len(real_stock_price)]
#plt.plot(real_stock_price)
#plt.plot(predicted, color = 'green')

history = [x for x in X_train]

predictions = list()
for t in range(len(real_stock_price)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    if t < 10:
        yhat = output[0]
        predictions.append(yhat)
        obs = real_stock_price[t]
        history.append(obs)
    else:
        yhat = output[0]
        predictions.append(yhat)
        obs = predictions[t]
        history.append(obs)
    
        
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(real_stock_price, predictions)
print('Test MSE: %.3f' % error)
# plot
real_stock_price = real_stock_price[10:]
predictions = predictions[10:]
plt.plot(real_stock_price)
plt.plot(predictions, color='red')
plt.show()

# Determining accuracy
def hilo(stocks):
    predictions = []
    for i in range(1, len(stocks)):
        if stocks[i] >= stocks[i - 1]:
            predictions.append(1)
        else:
            predictions.append(0)
            
    return predictions
    
real_hilo = np.array(hilo(real_stock_price))
predicted_hilo = np.array(hilo(predictions))

correct = (real_hilo == predicted_hilo)

accuracy = correct.sum() / correct.size
print(accuracy)

from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(real_hilo, predicted_hilo).ravel()

print("Precision: ", tp/(tp + fp))
print("Recall: ", tp/(tp + fn))
    
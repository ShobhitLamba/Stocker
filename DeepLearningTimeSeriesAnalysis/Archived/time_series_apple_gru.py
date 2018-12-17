#Part 1 - Data Preprocessing

#Importing the libraries
import numpy as np
import pandas as pd
from keras.utils import to_categorical

#Importing the training set
dataset_train = pd.read_csv('Datasets/Archived/AAPL_train.csv')
training_set = dataset_train.iloc[:, 4:5].values

#Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

#Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
y_temp = []
for i in range(100, 4330):
    X_train.append(training_set_scaled[i-100:i, 0])
    y_temp.append(training_set_scaled[i, 0])

y_temp = np.insert(y_temp, 0, training_set_scaled[99], axis = 0)
length_1 = len(y_temp)  
  
for i in range(1, length_1):
    if y_temp[i-1] > y_temp[i]:
        y_train.append(0)
    else:
        y_train.append(1)
        
X_train = np.array(X_train)
#y_train= to_categorical(y_train, num_classes=len(np.unique(y_train)))

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#Part 2 - Building the model

#Importing the keras libraries and packages  
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU, Conv1D, BatchNormalization, Activation
from keras.layers import Dropout

# Initializing the RNN
regressor = Sequential()

regressor.add(Conv1D(filters = 128, kernel_size = 1, activation = 'relu', input_shape = (X_train.shape[1], 1)))
regressor.add(BatchNormalization())
regressor.add(Activation('relu'))

#Adding the first LSTM layer and some Dropout regularisation
regressor.add(GRU(units = 100))
regressor.add(Dropout(0.5))

#Adding the output layer
regressor.add(Dense(units = 50, activation = 'linear'))
regressor.add(Dense(units = 1, activation = 'sigmoid'))

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'binary_crossentropy')

regressor.summary()

#Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs = 5, batch_size = 32)

# Getting the real stock price of 2018
dataset_test = pd.read_csv('Datasets/Archived/AAPL_test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

#Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['Close'], dataset_test['Close']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 100:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
y_test_temp = []
y_test = []
for i in range(100, 298):
    X_test.append(inputs[i-100:i, 0])
    y_test_temp.append(inputs[i-1, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted = regressor.predict_classes(X_test)

#Visualising the results
import matplotlib.pyplot as plt

plt.plot(real_stock_price, color = 'red', label = 'Real Stock Price')
plt.plot(predicted, color = 'blue', label = 'Predicted Stock Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

y_test_temp = np.insert(y_test_temp, 0, inputs[99], axis = 0)
length_2 = len(y_test_temp)

for i in range(1, length_2):
    if y_test_temp[i-1] > y_test_temp[i]:
        y_test.append(0)
    else:
        y_test.append(1)

#predicted = np.argmax(predicted, axis = -1)

from sklearn.metrics import precision_recall_fscore_support as score

precision, recall, fscore, support = score(y_test, predicted)
count = 0
for i in range(len(y_test)):
    if(y_test[i] == predicted[i]):
        count+=1

print('accuracy: ', count/len(y_test))
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))
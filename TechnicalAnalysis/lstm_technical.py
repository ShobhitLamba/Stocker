#Part 1 - Data Preprocessing

#Importing the libraries
import numpy as np
import pandas as pd
#from keras.utils import to_categorical

#Importing the training set
dataset_train = pd.read_csv('Datasets/BRK_fin_train.csv')
fin_data = dataset_train.iloc[:, 7:13].values
training_set = dataset_train.iloc[:, 4:5].values

#Feature Scaling
from sklearn.preprocessing import minmax_scale
#sc = minmax_scale(feature_range = (0, 1))
fin_data_scaled = minmax_scale(fin_data, feature_range = (0, 1))

#Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
y_temp = []
for i in range(1, 4482):
#    X_train.append(macd_scaled[i-100:i, 0])  
    y_temp.append(training_set[i-1, 0])

#y_temp = np.insert(y_temp, 0, training_set[0], axis = 0) 
#y_temp = np.insert(y_temp, 0, training_set[0], axis = 0)
  
for i in range(60, len(y_temp)):
    if y_temp[i-60] > y_temp[i]:
        y_train.append(0)
    else:
        y_train.append(1)

fin_data_scaled = fin_data_scaled[61:]              
X_train = np.array(fin_data_scaled)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#Part 2 - Building the model

#Importing the keras libraries and packages  
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv1D, BatchNormalization, Activation
from keras.layers import LSTM, Dropout

# Initializing the RNN
regressor = Sequential()

regressor.add(Conv1D(filters = 128, kernel_size = 1, input_shape = (X_train.shape[1], 1)))
regressor.add(BatchNormalization())
regressor.add(Activation('relu'))

# Adding the LSTM layers and some Dropout regularisation
regressor.add(LSTM(units = 100, return_sequences = True))
regressor.add(Dropout(0.5))

regressor.add(LSTM(units = 100))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1, activation = 'sigmoid'))

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'binary_crossentropy')

regressor.summary()

#Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

# Getting the real stock price of 2018
dataset_test = pd.read_csv('Datasets/BRK_fin_test.csv')
real_stock_price = dataset_test.iloc[:, 4:5].values

# Getting the predictions
dataset_total_y = np.insert(real_stock_price, 0, 169.23, axis = 0)
inputs_x = dataset_test.iloc[:, 7:13].values
inputs_x = minmax_scale(inputs_x, feature_range = (0, 1))
inputs_y = dataset_total_y.reshape(-1,1)
X_test = []
y_test_temp = []
y_test = []
for i in range(1, 198):
    y_test_temp.append(inputs_y[i-1, 0])
    
inputs_x = inputs_x[61:]    
X_test = np.array(inputs_x)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted = regressor.predict_classes(X_test)

#y_test_temp = np.insert(y_test_temp, 0, real_stock_price[0], axis = 0)
#y_test_temp = np.insert(y_test_temp, 0, real_stock_price[0], axis = 0)

for i in range(60, len(y_test_temp)):
    if y_test_temp[i-60] > y_test_temp[i]:
        y_test.append(0)
    else:
        y_test.append(1)
        
# Checking performance
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

import csv
rows = []
for i in range(len(y_test)):
    rows.append([str(y_test[i]), str(predicted[i])])

for row in rows:
    row[0] = row[0].replace('[', '').replace(']', '')
    row[1] = row[1].replace('[', '').replace(']', '')    

with open('BRK_60_pred.csv', 'w') as aapl:
    wr = csv.writer(aapl, lineterminator='\n')
    for row in rows:
#        print(row)
        wr.writerow(row)




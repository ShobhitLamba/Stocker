#Recurrent Neural Network


#Part 1 - Data Preprocessing

#Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing the training set
dataset_train = pd.read_csv('AAPL_train.csv')
training_set = dataset_train.iloc[:, 1:2].values

#Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

#Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(100, 4330):
    X_train.append(training_set_scaled[i-100:i, 0])
    if training_set_scaled[i] > training_set_scaled[i-7]:
        y_train.append(1)
    else:    
        y_train.append(0)
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#Part 2 - Building the model

#Importing the keras libraries and packages  
from keras.layers import Dense, BatchNormalization, GlobalAveragePooling1D
from keras.layers import LSTM, Permute, Conv1D, Activation, Reshape, Masking
from keras.layers import Dropout, Concatenate, Input, Model, multiply
from keras.utils import to_categorical

#from utils.layer_utils import AttentionLSTM

def squeeze_excite_block(input):
    filters = input._keras_shape[-1] # channel_axis = -1 for TF

    se = GlobalAveragePooling1D()(input)
    se = Reshape((1, filters))(se)
    se = Dense(filters // 16,  activation = 'relu', kernel_initializer = 'he_normal', use_bias = False)(se)
    se = Dense(filters, activation = 'sigmoid', kernel_initializer = 'he_normal', use_bias = False)(se)
    se = multiply([input, se])
    
    return se

ip = Input(shape = (100, 1))

x = Masking()(ip)
x = LSTM(100, return_sequences = True)(x)
x = Dropout(0.2)(x)

x = LSTM(50)(x)
x = Dropout(0.2)(x)

y = Permute((2, 1))(ip)
y = Conv1D(128, 8, padding = "same", kernel_initializer = "he_uniform")(y)
y = BatchNormalization()(y)
y = Activation("relu")(y)
y = squeeze_excite_block(y)

y = Conv1D(256, 5, padding = "same", kernel_initializer = "he_uniform")(y)
y = BatchNormalization()(y)
y = Activation("relu")(y)
y = squeeze_excite_block(y)

y = Conv1D(128, 3, padding = "same", kernel_initializer = "he_uniform")(y)
y = BatchNormalization()(y)
y = Activation("relu")(y)

y = GlobalAveragePooling1D()(y)

regressor = Concatenate(axis = -1)([x, y])

#Adding the output layer
regressor_final = Dense(units = 2, activation = 'softmax')(regressor)
regressor = Model(inputs = ip, outputs = regressor_final)

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

y_train = to_categorical(y_train, len(np.unique(y_train)))

#Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs = 20, batch_size = 32)

# Part 3 - Making the predictions and visualising the results

# Getting the real stock price of 2017
dataset_test = pd.read_csv('AAPL_test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

#Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 100:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(100, 298):
    X_test.append(inputs[i-100:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

##Visualising the results
#plt.plot(real_stock_price, color = 'red', label = 'Real Apple Stock Price')
#plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Apple Stock Price')
#plt.title('Apple Stock Price Prediction')
#plt.xlabel('Time')
#plt.ylabel('Apple Stock Price')
#plt.legend()
#plt.show()

# Determining accuracy
def hilo(stocks):
    predictions = []
    for i in range(7, len(stocks)):
        if stocks[i] >= stocks[i - 7]:
            predictions.append(1)
        else:
            predictions.append(0)
            
    return predictions
    
y_test = np.array(hilo(real_stock_price))

predicted_hilo = np.array([np.argmax(y, axis = None, out = None) for y in predicted_stock_price])
for i in range(len(predicted_hilo)):
    predicted_hilo[i] = abs(predicted_hilo[i] - 1)

accuracy = sum(1 for x, y in zip(y_test, predicted_hilo) if x == y) / float(len(y_test))
print(accuracy)

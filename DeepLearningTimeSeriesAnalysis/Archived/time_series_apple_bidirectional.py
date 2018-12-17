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
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#Part 2 - Building the RNN

#Importing the keras libraries and packages  
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.layers import LSTM, Bidirectional
from keras.layers import Dropout

# Initializing the RNN
regressor = Sequential()

#Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

##Adding a Bidirectional LSTM layer and some Dropout regularisation

regressor.add(Bidirectional(LSTM(units = 50), merge_mode = "concat"))
regressor.add(Dropout(0.2))

#Adding the output layer
regressor.add(Dense(units = 1))

#Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

#Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs = 25, batch_size = 32)

# serialize model to JSON
bidirectional_json = regressor.to_json()
with open("bidirectional.json", "w") as json_file:
    json_file.write(bidirectional_json)
# serialize weights to HDF5
regressor.save_weights("bidirectional.h5")
print("Saved bidirectional model to disk.")

# load json and create model
json_file = open('bidirectional.json', 'r')
bidirectional_model_json = json_file.read()
json_file.close()
loaded_regressor = model_from_json(bidirectional_model_json)
# load weights into new model
loaded_regressor.load_weights("bidirectional.h5")
print("Loaded bidirectional model from disk.")

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
predicted_stock_price = loaded_regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

#Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real Apple Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()

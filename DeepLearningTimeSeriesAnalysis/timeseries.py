from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, GRU, Bidirectional
from keras.models import Sequential
import lstm, time
#import numpy as np
import pandas as pd

# Importing the training set
X_train, y_train = lstm.load_data('Datasets/Archived/WFC_train_closed.csv', 50, True)
X_test, y_test = lstm.load_data('Datasets/Archived/WFC_test_closed.csv', 50, True)

#dates = pd.read_csv('Datasets/Archived/WFC_test.csv')
#dates = dates.iloc[:, 0:1].values

#for i in range(150):
    

#Step 2 Build Model
model = Sequential()

model.add(LSTM(
    input_dim=1,
    output_dim=50,
    return_sequences=True))
model.add(Dropout(0.2))

#model.add(LSTM(
#    input_dim=1,
#    output_dim=100,
#    return_sequences=True))
#model.add(Dropout(0.2))
#
#model.add(LSTM(
#    input_dim=1,
#    output_dim=100,
#    return_sequences=True))
#model.add(Dropout(0.2))

model.add(LSTM(
    100,
    return_sequences=False))
model.add(Dropout(0.2))

#model.add(Bidirectional(LSTM(
#    input_dim=1,
#    output_dim=50,
#    return_sequences=True)))
#model.add(Dropout(0.2))
#
#model.add(Bidirectional(LSTM(
#    100,
#    return_sequences=False)))
#model.add(Dropout(0.2))

model.add(Dense(
    output_dim=1))
model.add(Activation('linear'))

start = time.time()
model.compile(loss='mse', optimizer='rmsprop')
#print ('compilation time : ', time.time() - start)

#Step 3 Train the model
model.fit(
    X_train,
    y_train,
    batch_size=512,
    nb_epoch=1,
    validation_split=0.05)

X_test = X_test[:30]
y_test = y_test[:30]

# Step 4 - Plot the predictions!
prediction_len = 3
predictions = lstm.predict_sequences_multiple(model, X_test, 30, prediction_len)
lstm.plot_results_multiple(predictions, y_test, prediction_len)

#hilo_pred = []
#for prediction in predictions:
#    if prediction[0] > prediction[-1]:
#        hilo_pred.append(0)
#    else:
#        hilo_pred.append(1)
#
#        
#hilo_real = []
#for i in range(0, 147, prediction_len):
#    if y_test[i] > y_test[i + prediction_len]:
#        hilo_real.append(0)
#    else:
#        hilo_real.append(1)
#
##hilo_pred = hilo_pred[:-1]        
#from sklearn.metrics import precision_recall_fscore_support as score
#
#precision, recall, fscore, support = score(hilo_real, hilo_pred)
#count = 0
#for i in range(len(hilo_real)):
#    if(hilo_real[i] == hilo_pred[i]):
#        count+=1
#
#print('accuracy: ', count/len(hilo_real))
#print('precision: {}'.format(precision))
#print('recall: {}'.format(recall))
#print('fscore: {}'.format(fscore))
#print('support: {}'.format(support))

#predicted = []
#for i in range(len(predictions)):
#    for j in range(prediction_len):
#        predicted.append(predictions[i][j])
#    
#import csv
#rows = []
#y_test = y_test[:120]
#for i in range(len(y_test)):
#    rows.append([str(y_test[i]), str(predicted[i])])
#
#for row in rows:
#    row[0] = row[0].replace('[', '').replace(']', '')
#    row[1] = row[1].replace('[', '').replace(']', '')    
#
#with open('AAPL_predictions_tsa_60.csv', 'w') as aapl:
#    wr = csv.writer(aapl, lineterminator='\n')
#    for row in rows:
#        print(row)
#        wr.writerow(row)
##
##dates = []
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:28:24 2018

@author: Sakshi Panday

@Overview
This gets the output for all the patterns triggered of specified company for a particular day
"""
import time
start_time = time.time()

import pandas as pd
import talib
import csv
from statistics import mean

# =============================================================================
# Function to write Dictionary into CSV
# =============================================================================
def writeDictToCSV(myDict, filename):
    w = csv.writer(open(filename+".csv", "w"), lineterminator='\n')
    w.writerow(['Pattern', 'Prediction', 'Accuracy'])
    for key, val in myDict.items():
        w.writerow([key, val[0], val[1]])
        
# =============================================================================
# generates report with prediction and accuracy including the average prediction       
# =============================================================================
def generatePredictionReport(dicResults):
    high = []
    low = []
    predictions = {}
    for pattern in dicResults.keys():
        highConf = dicResults[pattern][1]
        lowConf = dicResults[pattern][2]
        if(highConf>lowConf):
            predictions[pattern] = ('HIGH', highConf)
        else:
            predictions[pattern] = ('LOW', lowConf)
        high.append(highConf) 
        low.append(lowConf)
    AvgHigh = mean(high)
    AvgLow = mean(low)
    if(AvgHigh>AvgLow):
        predictions['Weighted Average'] = ('HIGH', AvgHigh)
    else:
        predictions['Weighted Average'] = ('LOW', AvgLow)
        
    return predictions
    

# =============================================================================
# This function calculates the accuracy for positive and negative triggers
# =============================================================================
def patternPrediction(stockData, predictionInfo, timeGap = 0):
    accuracy = 0
    negativeTriggers = 0
    positiveTriggers = 0
    negativeAccuracy = 0
    positiveAccuracy = 0
    for num,i in enumerate(predictionInfo):
        if i < 0 and num + timeGap <  len(predictionInfo):
            if stockData['Close'][num] > stockData['Close'][num+timeGap]:
                accuracy += 1
                negativeAccuracy += 1
            negativeTriggers += 1
        elif i > 0 and num + timeGap <  len(predictionInfo):
            if stockData['Close'][num] < stockData['Close'][num+timeGap]:
                accuracy += 1
                positiveAccuracy += 1
            positiveTriggers += 1
            
    if negativeTriggers == 0 and positiveTriggers != 0:
        return accuracy/(negativeTriggers + positiveTriggers), positiveAccuracy/positiveTriggers, 0
    if positiveTriggers == 0 and negativeTriggers != 0:
        return accuracy/(negativeTriggers + positiveTriggers), 0 ,negativeAccuracy/negativeTriggers
    return accuracy/(negativeTriggers + positiveTriggers), positiveAccuracy/positiveTriggers, negativeAccuracy/negativeTriggers

# =============================================================================
# Fetches all those patterns that trigger on the current date
# =============================================================================
def getTriggeredPatternsPrediction(stockData, date, timeGap = 1):
    patternFuncs = talib.get_function_groups()['Pattern Recognition']
    patternAnalysis = {}
    patternAccuracy = {}
    for patternFunc in patternFuncs:
        patternAnalyzer = getattr(talib, patternFunc)
        predictionInfo = patternAnalyzer(stockData['Open'], stockData['High'], stockData['Low'], stockData['Close'])
        try:
            predictionInfo[stockData[stockData['Date'] == date].index[0]]
        except:
            print('The date given is a non-trading day (i.e. Weekend)')
            return pd.DataFrame({})
        if(predictionInfo[stockData[stockData['Date'] == date].index[0]] != 0):
            print(patternFunc)            
            print('Accuracy:', patternPrediction(stockData, predictionInfo, timeGap))
            patternAccuracy[patternFunc] = patternPrediction(stockData, predictionInfo, timeGap)
#            newDF = stockData
#            newDF['Action'] = predictionInfo
#            newDF.to_csv(patternFunc+'.csv', index=False)
            patternAnalysis[patternFunc] = predictionInfo.tail(1)
    patternAnalysis = pd.DataFrame(patternAnalysis)

    return pd.DataFrame(patternAccuracy)
#    return triggeredPatternsPrediction

# =============================================================================
# This function helps to get the Prediction (high/low) as well as Accuracy of
# the prediction for every pattern triggered of the company at given date 
# =============================================================================
def getPatternData(company, date):
    stockData = pd.read_csv("Stock Data/"+company+".csv")
#    print(stockData[stockData['Date'] == date].index[0])
    triggeredPatternsPrediction = getTriggeredPatternsPrediction(stockData, date)
    if not triggeredPatternsPrediction.empty:
        predictionReport = generatePredictionReport(triggeredPatternsPrediction)
        writeDictToCSV(predictionReport, 'patternPrediction_'+company+'_'+date )
    else:
        print('no patterns triggered')
    
    
for i in range(10,31):
    print('___'+str(i)+'___')
    getPatternData('GOOGL_fulldata', '2018-01-'+str(i))
    
print ("My program took", time.time() - start_time, "to run")
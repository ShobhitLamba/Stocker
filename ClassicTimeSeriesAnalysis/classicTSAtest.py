# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 21:12:03 2018

@author: Sakshi Panday

@Overview
"""

import pandas as pd
import classicTSA as ctsa


stockData = pd.read_csv("Stock Data/AAPL_fulldata.csv")

closePrice = stockData['Close'].tolist()
days = 30
lastPrice = closePrice[-days-1]
realPrice = closePrice[-days:]
trainPrice = closePrice[-180:-days]


p3 = ctsa.QuarterSAIRMAmodel(trainPrice, days-1)

p4 = ctsa.MonSAIRMAmodel(trainPrice, days-1)


import matplotlib.pyplot as plt
plt.plot(realPrice,'b')
plt.plot(p3, 'r')
plt.plot(p4, 'm')
plt.ylabel('price')
plt.show()
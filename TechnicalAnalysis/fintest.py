# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 01:32:04 2018

@author: Sakshi Panday

@Overview
"""

import time
start_time = time.time()

import finindicators as fi
import getBuySell as gbs
import pandas as pd
import numpy as np
from Prediction import predict

# =============================================================================
# Prepare the data with financial Indicators
# =============================================================================
df = pd.read_csv("Stock Data/AAPL_fulldata.csv")
df = fi.macd(df, 26, 12)
df = fi.stochastic_oscillator_d(df, 14)
df = fi.bollinger_bands(df, 20)
df = fi.moving_average(df, 20)
df = fi.accumulation_distribution(df, 14)
df = fi.chaikin_oscillator(df)
df = fi.commodity_channel_index(df,20)
df = fi.coppock_curve(df,20)
df = fi.keltner_channel(df,20)
df = fi.donchian_channel(df,20)
df = fi.average_true_range(df, 20)
df = fi.average_directional_movement_index(df, 20, 25)
df = fi.money_flow_index(df, 20)
df = fi.vortex_indicator(df, 20)

#df.to_csv("Stock Data/datasets/WFC_fin_train.csv", sep=',')

#df = gbs.getMACDhl(df)
#df = gbs.getSOhl(df)
#df = gbs.getBBhl(df)
df = gbs.getRealhl(df, 15)
df = df.dropna()


# =============================================================================
# choose feature selected indicators and predict
# =============================================================================

#allIndicators = ['MACD_26_12', 'SO%d_14', 'BollingerB_20', 'Bollinger%b_20', 'MA_20', 'Acc/Dist_ROC_14', 'Chaikin', 'CCI_20', 'Copp_20', 'KelChM_20', 'KelChU_20', 'KelChD_20', 'Donchian_20', 'ATR_20', 'ADX_20_25', 'MFI_20', 'Vortex_20']
allSelectedIndicators = ['MACD_26_12', 'SO%d_14', 'Bollinger%b_20', 'Acc/Dist_ROC_14', 'Chaikin', 'CCI_20', 'Copp_20', 'KelChD_20', 'Donchian_20', 'ATR_20', 'ADX_20_25', 'MFI_20', 'Vortex_20']

'''supress version warnings'''
import warnings
warnings.filterwarnings("ignore")

predict(df, allSelectedIndicators)


'''
For each indicator seperately
'''
#for indicator in allIndicators:
#    predict(df, indicator)


#print ("My program took", time.time() - start_time, "to run")

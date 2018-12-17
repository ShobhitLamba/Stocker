# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 10:16:37 2018

@author: Sakshi Panday

@Overview
"""

import numpy as np

def getMACDhl(df):
    df['MACDhl'] = np.where(df['MACD_26_12'] <= df['MACDsign_26_12'], -1, 1)
    return df

def getSOhl(df):
    df['SOhl'] = np.where(df['SO%d_14'] >= 0.70, 1, np.where(df['SO%d_14'] <= 0.30, -1, 0))
    return df

def getBBhl(df):
    df['BBhl'] = np.where(df['BollingerB_20']<df['Close'], 1, np.where(df['Bollinger%b_20'] > df['Close'], -1, 0))
    return df

def getRealhl(df, days = 1):
    df['realHL'] = df['Close'] < df['Close'].shift(days)
    return df
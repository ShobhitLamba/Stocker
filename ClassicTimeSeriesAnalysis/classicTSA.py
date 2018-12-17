# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:08:59 2018

@author: Sakshi Panday

@Overview: This contains functions for all the Classic Time Series Analysis models
"""
# =============================================================================
# Monthly Seasonal Autoregressive Integrated Moving Average for trend
# and/or monthly seasonal components    
# =============================================================================
def ARMAmodel(data, days = 0):
    from statsmodels.tsa.arima_model import ARMA
    model = ARMA(data, order=(2, 1))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(data), len(data)+days)
    return(yhat)

# =============================================================================
# Autoregressive Integrated Moving Average for trend in time series    
# =============================================================================
def ARIMAmodel(data, days = 0):
    from statsmodels.tsa.arima_model import ARIMA
    model = ARIMA(data, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(data), len(data)+days, typ='levels')
    return(yhat)
    
# =============================================================================
# Monthly Seasonal Autoregressive Integrated Moving Average for trend
# and/or monthly seasonal components    
# =============================================================================
def MonSAIRMAmodel(data, days = 0):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(data), len(data)+days)
    return(yhat)
    

# =============================================================================
# Quarterly Seasonal Autoregressive Integrated Moving Average for trend
# and/or quarterly seasonal components    
# =============================================================================
def QuarterSAIRMAmodel(data, days = 0):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(2, 2, 1, 4))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(data), len(data)+days)
    return(yhat)
    
    
# =============================================================================    
# The Holt Winter’s Exponential Smoothing (HWES) also called the Triple 
# Exponential Smoothing method models the next time step as an exponentially 
# weighted linear function of observations at prior time steps, taking trends 
# and seasonality into account.    
# =============================================================================
def HWESmodel(data, days = 0):
    # HWES example
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    model = ExponentialSmoothing(data)
    model_fit = model.fit()
    yhat = model_fit.predict(len(data), len(data)+days)
    return(yhat)
    
    

    
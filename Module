import numpy as np
import matplotlib.pyplot as plt
import os
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
client = Client(api_key,secret_key)
OHLC=((np.array(client.futures_klines(symbol='BTCBUSD',interval='1h',limit=100))[:,1:5]).astype(float))
H=OHLC[:,3]
##########################################################################################
########################################INDICATORS########################################
################################################################################################

##########ExponentialMovingAverage##########
def EMA(intervals, prices):
    weight = 2 / (intervals + 1)
    ema= np.zeros(len(prices))
    ema[0] = prices[0]

    for i in range(1, len(prices)):
        ema[i] = (prices[i] * weight) + (ema[i - 1] * (1 - weight))
    return ema

##########RAVI##########
def RAVI(first_EMA,Second_EMA,prices):
    EMA_first = EMA(first_EMA, prices)
    EMA_second = EMA(Second_EMA,prices)
    ravi=np.zeros(len(prices))
    for i in range(1,len(prices)):
        ravi[i]=(EMA_first[i]-EMA_second[i])/EMA_second[i]
    return ravi

##########TRUERANGE##########
def True_Range(OHLC_):
    TR=np.zeros(len(OHLC_))
    for i in range(1, len(OHLC_)):
        TR[i]=np.max([abs(OHLC_[i,0]-OHLC_[i,1]),abs(OHLC_[i,0]-OHLC_[i,2]),abs(OHLC_[i,2]-OHLC_[i,3])])
    return TR

##########AVERAGE TRUE RANGE##########
def Average_True_Range(intervals,OHLC):
    TR = True_Range(OHLC)
    ATR=np.zeros(len(OHLC))
    for i in range(1, len(OHLC)):
        if i >= 6:
            ATR[i]=np.mean(TR[i-intervals:i])
        else:
            ATR[i] = 0
    return ATR
##########AVERAGE TRUE RANGE TRAILING STOPS##########
def ATR_Trailing_Stops_BuyOrd(interval,coef,OHLC):
    ATR = Average_True_Range(interval,OHLC)
    SB=np.zeros(len(OHLC))
    for i in range(1,len(OHLC)):
        SB[i]=OHLC[:,3][i]-ATR[i]*coef
    return SB

def ATR_Trailing_Stops_SellOrd(interval,coef,OHLC):
    ATR = Average_True_Range(interval,OHLC)
    SL=np.zeros(len(OHLC))
    for i in range(1,len(OHLC)):
        SL[i]=OHLC[:,3][i]+ATR[i]*coef
    return SL

##########RSI gradual calculation##########
def increases_in_value(OHLC):
    up=np.array([])
    for i in range(0,len(OHLC)):
        if OHLC[i,3]>OHLC[i-1,3]:
            up=np.append(up,OHLC[i,3]-OHLC[i-1,3])
        else:
            up=np.append(up,0)
    return up

def drops_in_value(OHLC):
    lower=np.array([])
    for i in range(0,len(OHLC)):
        if OHLC[i,3]<OHLC[i-1,3]:
            lower=np.append(lower,OHLC[i-1,3]-OHLC[i,3])
        else:
            lower=np.append(lower,0)
    return lower

def EMA_upper(intervals, prices):
    up_values=increases_in_value(prices)
    weight = 2 / (intervals + 1)
    emau= np.zeros(len(up_values))
    if OHLC[0,3]>OHLC[0,0]:
        emau[0] = OHLC[0,3]-OHLC[0,0]
    else:
        emau[0]=0.00001

    for i in range(1, len(up_values)):
        emau[i] = (up_values[i] * weight) + (emau[i - 1] * (1 - weight))
    return emau

def EMA_lower(intervals, prices):
    low_values=drops_in_value(prices)
    weight = 2 / (intervals + 1)
    emal= np.zeros(len(low_values))
    if OHLC[0,3]<OHLC[0,0]:
        emal[0] = OHLC[0,0]-OHLC[0,3]
    else:
        emal[0]=0.00001

    for i in range(1, len(low_values)):
        emal[i] = (low_values[i] * weight) + (emal[i - 1] * (1 - weight))
    return emal

def Relative_Strength(intervals, prices):
    RS=np.zeros(len(OHLC))
    for i in range(1,len(OHLC)):
        RS[i]=(EMA_upper(intervals, prices)[i])/(EMA_lower(intervals, prices)[i])
    return RS 

def Relative_Strength_Index_EMA(intervals, prices):
    rsi=np.zeros(len(OHLC))
    for i in range(1,len(OHLC)):
        rsi[i]=100-(100/(1+Relative_Strength(intervals, prices)[i]))
    return rsi


################################################################################################
########################################ORDER CONDITIONS########################################
################################################################################################
def RAVI_sign_change_to_pos(first_EMA,Second_EMA,ravi):
    if ravi[-1]>0 and ravi[-2]<0:
        return True
    else:
        return False
def RAVI_sign_change_to_neg(first_EMA,Second_EMA,ravi):
    if ravi[-1]<0 and ravi[-2]>0:
        return True
    else:
        return False

def RAVI_sign_change_to_pos_last_int(first_EMA,Second_EMA,ravi):
    if ravi[-2]>0 and ravi[-3]<0:
        return True
    else:
        return False

def RAVI_sign_change_to_neg_last_int(first_EMA,Second_EMA,ravi):
    if ravi[-2]<0 and ravi[-3]>0:
        return True
    else:
        return False

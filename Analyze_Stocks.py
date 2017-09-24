# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:35:08 2017

@author: Boaz
"""

import talib as ta
from pandas_datareader import data as pdr
import pandas as pd
import fix_yahoo_finance as yf
import numpy as np
import matplotlib.pylab as plt
import os

def investigate_stock(stock,orders):
    plt.plot(stock)
    plt.plot(ta.MACD(stock,50,200,20)[0])
    plt.plot([0, 700],[0,0], 'k')
    plt.plot(ta.MOM(stock,200))
    plt.plot(ta.MOM(stock,50))
    for i in range(1,len(orders)):
        if orders[i-1] != orders[i] == "+":
            plt.plot(i,stock[i],'*r')
        if orders[i-1] != orders[i] == "-":
            plt.plot(i,stock[i],'*b')            
    

def loadStocks_msgpack(path):
    return pd.read_msgpack(path)

def CleanStocks(frame):
    return frame['Adj Close',:,:].dropna(axis=1)
    
def AnalyzeStock(stock):
    #return ''.join(list(map(lambda x: '-' if x > 0 else '+' if x<0 else '0',np.sign(np.diff(stock)))))
    #    movingaverage = ta.macd(stock.values,20,50)[0]
    #    momentum1 = ta.mom(stock.values,10)
    #    momentum2 = ta.mom(stock.values,40)
    #    return ''.join(list(map(lambda x: '+' if (x[0] > 0 and x[1] > 0 and x[2] > 0) else '-' if (x[0] <0 or x[1]<0 or x[2]<0)  else '0'
    #                            ,zip(movingaverage,momentum1,momentum2))))
    return ''.join(list(map(lambda x: '+' if x> 0 else '-' if x <0 else '0',ta.MOM(stock.values,10))))

def applyAux(order,stockVal):
    global position, Money
    if order == "+":        
            position += Money/stockVal
            Money = 0.0
    elif order == "-":
        Money += position*stockVal
        position = 0
    return Money+position*stockVal
           
def moving_average(a, n=3) :
    return ta.MA(a,n) 

def ApplyStockAnalysis(stock,analysis):   
    global position, Money
    position = 0.0
    Money = 100.0
    return np.array([100] + list(map(applyAux,analysis,stock[1:])))

markets = ['nasdaq', 'nyse', 'amex', 'lse']    
market = markets[0]
path = r'C:\Users\Boaz\Documents\stocks-master\{}.msg'.format(market)
data = pd.read_msgpack(path)
data =  CleanStocks(data)
results = dict()
Money = 100.0
position = 0.0   
for stock in data:        
    analysis = AnalyzeStock(data[stock])
    worth = ApplyStockAnalysis(data[stock],analysis)
    results[stock] = [data[stock].values/data[stock][0]*100,worth]
    '''
    plt.plot(orders)
    plt.legend(['stock','algo'])
    plt.title('Normalized graph for stock "A" VS Algo')

    '''
success = [(s,results[s][1],results[s][1][-1],results[s][0][-1]) for s in results if results[s][1][-1] > 140]
mediocre = [(s,results[s][1],results[s][1][-1],results[s][0][-1]) for s in results if 100<results[s][1][-1] <= 140]
fail = [(s,results[s][1],results[s][1][-1],results[s][0][-1]) for s in results if results[s][1][-1] <100]
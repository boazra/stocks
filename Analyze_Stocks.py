# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:35:08 2017

@author: Boaz
"""

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import matplotlib.pylab as plt
import os

def loadStocks_msgpack(path):
    return pd.read_msgpack(path)

def CleanStocks(frame):
    return frame['Adj Close',:,:].dropna(axis=1)
    
def AnalyzeStock(stock):
    stock_orders = ""
    for i in range(len(stock)):
        if i >0:
            if stock[i] > stock[i-1]:
                stock_orders += "-"
            elif stock[i] < stock[i-1]:
                stock_orders += "+"
            else:
                stock_orders += "0"
    return stock_orders

def ApplyStockAnalysis(stock,analysis):
    Money = 100.0
    position = 0.0
    day = 1
    worth = []
    for order in analysis:                
        if order == "+":
                        
            position += Money/stock[day]
            Money = 0.0
        elif order == "-":
            Money += position*stock[day]
            position = 0
        worth.append(Money + position*stock[day])
        day += 1            
    return Money + position*stock[-1],worth
                                        
markets = ['nasdaq', 'nyse', 'amex', 'lse']    
market = markets[0]
path = r'C:\Users\Boaz\Documents\stocks\work with stocks\data\{}.msg'.format(market)
data = pd.read_msgpack(path)
data =  CleanStocks(data)
stock = data['A']
analysis = AnalyzeStock(stock)
revenue,orders = ApplyStockAnalysis(stock,analysis)
plt.plot(stock.values/data['A'][0]*100)
plt.plot(orders)
plt.legend(['stock','algo'])
plt.title('Normalized graph for stock "A" VS Algo')

    
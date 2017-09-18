# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 16:12:15 2017

@author: Boaz
"""
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import matplotlib.pylab as plt
import os

yf.pdr_override()

def loadStocks():
    markets = ['NASDAQ', 'NYSE', 'LSE', 'AMEX']
    stocks = dict()
    for market in markets:
        with open('{}.txt'.format(market),'r') as f:
            stocks[market] = f.read().split(',')
    return stocks

stocklist = loadStocks()            
path = os.path.dirname(__file__)
for market in stocklist:
    data = pdr.get_data_yahoo(stocklist[market],"2015-01-01")
    data.to_msgpack(r'C:\Users\Boaz\Documents\stocks\work with stocks\{}.msg'.format(market))

'''

short_range=7
intermediate_range = 44
long_range = 252

font = {'family' : 'DejaVu Sans',        
        'size'   : 26}
plt.rc('font', **font)
plt.ioff()

with open('Stock Review.txt','a+') as f:
    with open('Interesting Stocks.txt','a+') as f2:
        f.seek(0)
        reviewed_Stocks = [x.split(',')[0] for x in f.readlines()[1:]]        
        if f.tell() == 0:
            f.write('Name,PE,change_pct,last,short_ratio,time,volatility_mean,volatility_std,week,2month,year,2year\n')
        for market in stocklist:
            count = 0
            total = stocklist[market].__len__()
            for stock in stocklist[market]:
                if stock in reviewed_Stocks:
                    total -=1
                    continue
                try:
                    data = pdr.get_data_yahoo(stock,"2015-01-01")
                    quotes = pdr.get_quote_yahoo(stock)
                    graph = data.values[:,4]
                except:
                    print()
                    print('stock {} could not be loaded'.format(stock))
                if graph.__len__() < 252*2:
                    print()
                    print('stock {} is too new'.format(stock))
                    f.write(stock + ',,,,,,,,,,,too new\n')
                    count += 1
                    continue
                volatility = np.diff(graph)/graph[1:]*100
                short_range_change = graph[-1]/graph[-short_range]
                intermediate_range_change = graph[-1]/graph[-intermediate_range]
                long_range_change = graph[-1]/graph[-long_range]
                two_year_change = graph[-1]/graph[-2*long_range]            
                stock_string =  quotes.to_csv().split('\n')[1] + ',{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n'.format(volatility.mean(),                                          
                                              volatility.std(),short_range_change,intermediate_range_change,long_range_change,two_year_change)           
                f.write(stock_string)
                if intermediate_range_change > 1 and long_range_change > 1:
                    f2.write(stock + ',')
                    plt.close('all')
                    plt.figure(stock,(20,10))
                    plt.plot(graph)
                    plt.title('stock name = {}. year change = {:.2f}%'.format(stock,(long_range_change-1)*100))
                    plt.savefig(path + '/Images/{}.jpg'.format(stock))
                    print()
                    print('Stock {} was interesting. 52w change = {}'.format(stock,long_range_change))
                else:
                    print()
                    print('Stock {} was not interesting. year = {:.2f}%, 2month = {:.2f}%'.format(stock,(long_range_change-1)*100,(intermediate_range_change-1)*100))
                    count += 1
                    print('finished stock {}/{}'.format(count,total))
'''
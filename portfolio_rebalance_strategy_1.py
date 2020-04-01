import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import my_ta_lib as ta
import datetime
import copy

freq = 'monthly'

tickers = ["MMM","AXP","T","BA","CAT","CVX","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UTX","UNH","VZ","V","WMT","DIS"]

ohlc_mon = {} # directory with ohlc value for each stock            
attempt = 0 # initializing passthrough variable
drop = [] # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        try:
            ohlc_mon[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(2900),datetime.date.today()-datetime.timedelta(100),interval='m')
            ohlc_mon[tickers[i]].dropna(inplace = True)
            drop.append(tickers[i])       
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1
 
tickers = ohlc_mon.keys() # redefine tickers variable after removing any tickers with corrupted data

#BenchmarkStrategy: Buy and Hold DJI Index

DJI = pdr.get_data_yahoo('^DJI', datetime.date.today()-datetime.timedelta(2900),datetime.date.today()-datetime.timedelta(100),interval='m')
DJI['mon_ret'] = DJI['Adj Close'].pct_change(1)
dji_cagr = ta.get_cagr(DJI, freq)
dji_sharpe = ta.get_sharpe(DJI,freq,risk_free_rate=0.0)
dji_dd = ta.get_max_drawdown(DJI) / 100

#Monthly return for each stock
ohlc_dict = copy.deepcopy(ohlc_mon)
return_df = pd.DataFrame()
for ticker in tickers:
    print('Calculating return for ', ticker)
    return_df[ticker] = ohlc_dict[ticker]['Adj Close'].pct_change(1)

import strategies as strg
pf = strg.pfolio(return_df, tickers, 20, 4)



def CAGR(DF):
    '''function to calculate the Cumulative Annual Growth Rate of a trading strategy'''
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

stgy_cagr = CAGR(return_df)
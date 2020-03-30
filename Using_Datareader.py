import pandas as pd
import pandas_datareader.data as pdr
import datetime as dt
import time

tickers = ["ASIANPAINT.NS","ADANIPORTS.NS","AXISBANK.NS","BAJAJ-AUTO.NS",
           "BAJFINANCE.NS","BAJAJFINSV.NS","BPCL.NS","BHARTIARTL.NS",
           "INFRATEL.NS","CIPLA.NS","COALINDIA.NS","DRREDDY.NS","EICHERMOT.NS",
           "GAIL.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS","HEROMOTOCO.NS",
           "HINDALCO.NS","HINDPETRO.NS","HINDUNILVR.NS","HDFC.NS","ITC.NS",
           "ICICIBANK.NS","IBULHSGFIN.NS","IOC.NS","INDUSINDBK.NS","INFY.NS",
           "KOTAKBANK.NS","LT.NS","LUPIN.NS","M&M.NS","MARUTI.NS","NTPC.NS",
           "ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBIN.NS","SUNPHARMA.NS",
           "TCS.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TITAN.NS",
           "UPL.NS","ULTRACEMCO.NS","VEDL.NS","WIPRO.NS","YESBANK.NS","ZEEL.NS","Chutiya.ns"]

start = pd.to_datetime('2018-01-01')
end = pd.to_datetime('2019-09-01')

stock_cp = pd.DataFrame()
attempt = 0
drop = []

while len(tickers) != 0 and attempt <= 6 :
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)) :
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('Working @ :', current_time)
        try :
            temp = pdr.get_data_yahoo(tickers[i], start, end)
            temp.dropna(inplace = True)
            stock_cp[tickers[i]] = temp['Adj Close']
            drop.append(tickers[i])
        except :
            print(tickers[i],": failed to get data, retrying....")
            continue
    attempt += 1

print(stock_cp.head())
#print(tickers)
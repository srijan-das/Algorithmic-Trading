import pandas as pd
import numpy as np
import pandas_datareader.data as pdr

tickers = ['IOC.NS','ICICIBANK.NS','LT.NS','HDFCBANK.NS','TCS.NS','BHARTIARTL.NS','TATACOMM.NS','COALINDIA.NS','ONGC.NS','SBIN.NS','TATASTEEL.NS','VEDL.NS','NTPC.NS','M&M.NS','PNB.NS','RELIANCE.NS','ITC.NS','BPCL.NS','HINDPETRO.NS','HINDALCO.NS','ADANIENT.NS']

start = pd.to_datetime('2014-01-01')
end = pd.to_datetime('2019-12-31')

ohlcv_dict = {}
attempts = 0
drop = []

while len(tickers) != 0 and attempts < 5 :
    tickers = [j for j in tickers if j not in drop]
    for tick in tickers:
        try:
            print("Fetching ", tick)
            ohlcv_dict[tick] = pdr.get_data_yahoo(tick, start, end)
            drop.append(tick)
        except:
            print('Unable to fetch {}. Retrying...'.format(tick))
            continue
    attempts += 1
    
tickers = drop
drop = []
my_money = 10000.0
start_balance = my_money

for tick in tickers:
    ohlcv_dict[tick]['dly_ret'] = ohlcv_dict[tick]['Adj Close'].pct_change(1)
    ohlcv_dict[tick]['cum_ret'] = ohlcv_dict[tick]['Adj Close'] / ohlcv_dict[tick]['Adj Close'][0]

dly_ret = pd.DataFrame()
cum_ret = pd.DataFrame()
adj_close = pd.DataFrame()

for tick in tickers:
    dly_ret[tick] = ohlcv_dict[tick]['dly_ret']
    cum_ret[tick] = ohlcv_dict[tick]['cum_ret']
    adj_close[tick] = ohlcv_dict[tick]['Adj Close']
    
portfolio = pd.DataFrame(columns = tickers)

for i in range(5) :
        portfolio = portfolio.append({tick:0}, ignore_index = True)

for tick in tickers:
    portfolio[tick] = [0.0,0.0,0.0,0.0,0.0]

portfolio.set_index(pd.Series(['No. Of Stocks', 'Total Money Invested', 'Last Bought At','Current Value','Current Returns']), inplace = True)

portfolio['SB'] = 0.0

# Works Well
def add_stocks(port, closes, tick, money_alloted, index) :
    if money_alloted > 0.0 and money_alloted >= closes[tick][index]:
        port[tick][0] = port[tick][0] + int(money_alloted / closes[tick][index])
        port[tick][1] = port[tick][1] + int(money_alloted / closes[tick][index]) * closes[tick][index]
        port[tick][2] = closes[tick][index]
        port[tick][3] = port[tick][0] * closes[tick][index]
        if port[tick][1] != 0:
            port[tick][4] = (port[tick][3] - port[tick][1]) / port[tick][1]
        else:
            port[tick][4] = 0
        print("Bought {} shares of {} at Rs. {}".format(port[tick][0], tick, closes[tick][index]))
        return port
    else:
        return port

# works
def update_portfolio(port, closes, tick, index) :
    port[tick][3] = port[tick][0] * closes[tick][index]
    if port[tick][1] != 0:
        port[tick][4] = (port[tick][3] - port[tick][1]) / port[tick][1]
    else:
        port[tick][4] = 0
    return port

def sell_stocks(port, closes, tick, index) :
    if port[tick][0] > 0 :
        print("Sold {} shares of {} at Rs. {}".format(port[tick][0], tick, closes[tick][index]))
        port['SB'][0] = port[tick][0] * closes[tick][index]
        port[tick][0] = 0
        port[tick][1] = 0
        port[tick][2] = 0
        port[tick][3] = 0
        port[tick][4] = 0
        return port
    else:
        return port

def money_allot(money, amount):
    if money >= amount :
        return {'amt':amount,'bal':money-amount}
    else:
        return {'amt':0.0,'bal':money}

each_inv = 1000.00

print('\n\n\n')

for i in range(len(adj_close['IOC.NS'])) :
    to_add = cum_ret.iloc[i].sort_values(ascending=False).index.tolist()[:10]
    if i == 0 :
        for tic in to_add:
            t = money_allot(my_money, each_inv)
            allot = t['amt']
            my_money = t['bal']
            portfolio = add_stocks(portfolio, adj_close, tic, allot, i)
    else :
        for tick in tickers: #Updating Cycle
            portfolio = update_portfolio(portfolio, adj_close, tick, i)
        to_rem = portfolio.iloc[4].sort_values(ascending=True).index.tolist()[:5]
        for tic in to_rem :
            portfolio = sell_stocks(portfolio, adj_close, tic, i)
            my_money = my_money + portfolio['SB'][0]
            portfolio['SB'][0] = 0.0
        for tic in to_add:
            t = money_allot(my_money, each_inv)
            allot = t['amt']
            my_money = t['bal']
            portfolio = add_stocks(portfolio, adj_close, tic, allot, i)

for tic in tickers :
    portfolio = sell_stocks(portfolio, adj_close, tic, i)
    my_money = my_money + portfolio['SB'][0]
    portfolio['SB'][0] = 0.0

ending_balance = my_money + portfolio.iloc[3].sum()

print('\n\n\n')
print("Starting Balance Rs. {} on {}".format(start_balance, start))
print("End Balance Rs. {} on {}".format(ending_balance, end))
print("%Returns = ",((ending_balance - start_balance) / start_balance)*100,"%")
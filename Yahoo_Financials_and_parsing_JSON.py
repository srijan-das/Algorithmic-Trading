from yahoofinancials import YahooFinancials
import pandas as pd

cp_tickers = ['AMZN','AAPL','MSFT', 'CSCO', 'NVDA']#, 'AMZN', ]

close_prices = pd.DataFrame()
start = '2018-01-01'
end = '2019-01-01'
attempts = 0
drop = []

while len(cp_tickers) != 0 and attempts <= 5 :
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)) :
        try:
            yahoo_financials = YahooFinancials(cp_tickers[i])
            
            json_obj = yahoo_financials.get_historical_price_data('2017-01-01','2018-01-01',time_interval='daily')
            
            ohlv = pd.DataFrame(json_obj[cp_tickers[i]]['prices'])
            
            ohlv = ohlv.set_index('formatted_date')
            
            close_prices[cp_tickers[i]] = ohlv['adjclose']
            
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i]," :failed to fetch data...retrying")
            continue
    attempts +=1

print(close_prices.head())
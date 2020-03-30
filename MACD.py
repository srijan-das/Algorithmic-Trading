import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import macd



ticker = 'MSFT'
msft = pdr.get_data_yahoo(ticker, pd.to_datetime('2013-01-01'), pd.to_datetime('2018-01-01'))
'''
msft['Daily Returns'] = msft['Adj Close'].pct_change(1)
msft['Cumulative Returns'] = msft['Adj Close'] / msft['Adj Close'][0]
'''

msft_macd = macd.get_macd(msft)
msft_macd.plot()
plt.legend()
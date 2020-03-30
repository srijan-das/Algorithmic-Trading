import pandas_datareader.data as pdr
import pandas as pd
import atr
import boll_bands
import matplotlib.pyplot as plt

ticker = 'AAPL'
start = pd.to_datetime('2015-01-01')
end = pd.to_datetime('2018-01-01')

aapl = pdr.get_data_yahoo(ticker, start, end)

aapl_atr = atr.get_atr(aapl, span= 50)

appl_bb = boll_bands.get_boll_bands(aapl, span = 20, multiplier = 2)

appl_bb.plot()
aapl['Adj Close'].plot()
plt.legend()
plt.show()

aapl['Volume'].plot(kind='bar')
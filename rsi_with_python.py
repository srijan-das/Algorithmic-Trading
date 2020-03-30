import pandas_datareader.data as pdr
import pandas as pd
import rsi
import matplotlib.pyplot as plt

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2012-01-01'), pd.to_datetime('2018-01-01'))

aapl_rsi = rsi.get_rsi(aapl, span = 14)

plt.figure(figsize = (18,5))
aapl_rsi.plot()
plt.axhline(y = 30, c = 'g')
plt.axhline(y = 70, c = 'r')
aapl['Adj Close'].plot()
plt.legend()
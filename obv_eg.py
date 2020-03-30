import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import pandas as pd
import obv

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2017-01-01'), pd.to_datetime('2018-01-01'))

aapl_obv = obv.get_obv(aapl)

plt.figure(figsize=(12,4))
aapl_obv.plot(kind='bar')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12,4))
aapl['Adj Close'].plot()
plt.show()
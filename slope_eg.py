import pandas_datareader.data as pdr
import pandas as pd
import slope

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2017-01-01'), pd.to_datetime('2018-01-01'))

aapl_slope = slope.get_slope(aapl)

aapl_slope.plot()
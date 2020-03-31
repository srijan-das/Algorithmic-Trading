import pandas as pd
import pandas_datareader.data as pdr
import my_ta_lib as ta

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2014-01-01'), pd.to_datetime('2019-01-01'))

aapl_cagr = ta.get_cagr(aapl)


import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import adx

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2017-01-01'), pd.to_datetime('2018-01-01'))

aapl_adx = adx.get_adx(aapl, 14)
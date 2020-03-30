from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key='XXEX8093CLK4YJNB', output_format = 'pandas')

data, meta_data = ts.get_intraday('GOOGL', interval='1min')
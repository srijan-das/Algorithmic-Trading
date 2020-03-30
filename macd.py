def get_macd(df, slow_span=26, fast_span=12, signal_span=9):
    '''
    Note : Should contain column 'Adj Close'
    '''
    df_copy = df
    df_copy['MA Fast'] = df_copy['Adj Close'].ewm(span=fast_span, min_periods = fast_span).mean()
    df_copy['MA Slow'] = df_copy['Adj Close'].ewm(span=slow_span, min_periods = slow_span).mean()
    
    df_copy['MACD'] = df_copy['MA Fast'] - df_copy['MA Slow']
    df_copy['MACD Signal'] = df_copy['MACD'].ewm(span=signal_span, min_periods = signal_span).mean()
    df_copy.dropna(inplace = True)
    
    return df_copy[['MACD','MACD Signal','Adj Close']]
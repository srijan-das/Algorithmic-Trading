def get_atr(data, span = 20) :
    '''
    dataframe should have column 'Adj Close','High','Low'
    '''
    df = data.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis = 1, skipna = False)
    df['ATR'] = df['TR'].rolling(span).mean()

    return df[['ATR','TR']]
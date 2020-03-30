def get_boll_bands(data, span=20, multiplier=2) :
    '''
    data should have 'Adj Close'
    Also returns BB range
    '''
    df = data.copy()

    df['MA'] = df['Adj Close'].rolling(span).mean()
    df['std_rolling'] = df['Adj Close'].rolling(span).std()

    df['BB_up'] = df['MA'] + df['std_rolling'] * multiplier
    df['BB_down'] = df['MA'] - df['std_rolling'] * multiplier
    df['BB_range'] = df['BB_up'] - df['BB_down']

    return df[['MA','BB_up','BB_down','BB_range']].dropna()
import pandas as pd
import numpy as np
import statsmodels.api as sm
from stocktrends import Renko


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

def get_renko_df(data, days = 120, brick = -1) :
    '''
    Supply normal yahoo DataFrame. Columns are renamed. \n
    brick size will be determined by ATR, unless specified otherwise
    '''
    df = data.copy()
    df.reset_index(inplace=True)
    df.drop('Close', axis=1, inplace=True)
    df.columns = ['date', 'high', 'low', 'open', 'volume', 'close']

    renko_df = Renko(df)

    if brick == -1 :
        renko_df.brick_size = round(get_atr(data, span = days)['ATR'][-1], 0)
    else :
        renko_df.brick_size = brick

    return renko_df.get_ohlc_data()

def get_slope(data, column = 'Adj Close', periods = 5) :
    '''
    Returns NP array
    '''
    n = periods
    series = data[column]
    slopes = [i*0 for i in range(n-1)]

    for i in range(n, len(series)+1) :
        y = series[i-n:i]
        x = np.array(range(n))

        y_scaled = (y - y.min()) / (y.max() - y.min())
        x_scaled = (x - x.min()) / (x.max() - x.min())

        x_scaled = sm.add_constant(x_scaled)

        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return pd.DataFrame(np.array(slope_angle), columns=['Slope for consecutive {} periods'.format(periods)])

def get_obv(data) :
    df = data.copy()
    '''
    Should contain 'Volume'
    '''
    df['Daily Return'] = df['Adj Close'].pct_change()
    df['Direction'] = np.where(df['Daily Return'] >= 0, 1, -1)
    df['Direction'][0] = 0
    df['Adj Volume'] = df['Direction'] *df['Volume']
    df['obv'] = df['Adj Volume'].cumsum()
    return df['obv']

def get_adx(DF,span = 14):
    "function to calculate ADX"
    df2 = DF.copy()
    df2['TR'] = get_atr(df2,span)['TR'] #the period parameter of atr.get_atr function does not matter because period does not influence TR calculation
    df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < span:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == span:
            TRn.append(df2['TR'].rolling(span).sum().tolist()[span])
            DMplusN.append(df2['DMplus'].rolling(span).sum().tolist()[span])
            DMminusN.append(df2['DMminus'].rolling(span).sum().tolist()[span])
        elif i > span:
            TRn.append(TRn[i-1] - (TRn[i-1]/span) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/span) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/span) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum']=df2['DIplusN']+df2['DIminusN']
    df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*span-1:
            ADX.append(np.NaN)
        elif j == 2*span-1:
            ADX.append(df2['DX'][j-span+1:j+1].mean())
        elif j > 2*span-1:
            ADX.append(((span-1)*ADX[j-1] + DX[j])/span)
    df2['ADX']=np.array(ADX)
    return df2['ADX']

def get_rsi(data, span = 14) :
    '''
    Should have Adj Close as column
    '''
    n = span
    df = data.copy()
    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['delta'] > 0, df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0, abs(df['delta']), 0)
    
    avg_gain = []
    avg_loss = []

    gain = df['gain'].tolist()
    loss = df['loss'].tolist()

    for i in range(len(df)) :
        if i < n :
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n :
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n :
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

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

    return df[['MA','BB_up','BB_down','BB_range']]

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

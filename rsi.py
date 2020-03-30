import pandas as pd
import numpy as np

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
    return df['RSI'].dropna()
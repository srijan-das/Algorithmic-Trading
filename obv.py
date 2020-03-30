import pandas as pd
import numpy as np

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
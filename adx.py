import atr
import pandas as pd
import numpy as np

def get_adx(DF,span = 14):
    "function to calculate ADX"
    df2 = DF.copy()
    df2['TR'] = atr.get_atr(df2,span)['TR'] #the period parameter of atr.get_atr function does not matter because period does not influence TR calculation
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
    return df2['ADX'].dropna()

import pandas_datareader.data as pdr
import pandas as pd

aapl = pdr.get_data_yahoo('AAPL', pd.to_datetime('2017-01-01'), pd.to_datetime('2018-01-01'))
aapl_adx = get_adx(aapl, 14)

print(aapl_adx.head())
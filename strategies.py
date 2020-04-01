import pandas as pd
import numpy as np

def pfolio(data, tickers, no_of_stocks, stocks_to_axe, include_portfolio_stocks = False) :
    '''
    data = DataFrame containing Monthly Returns of stocks\n
    Works by rebalancing portfolio every month by removing a number of poorest performing stocks and replacing them with best performing stocks\n
    All stocks have equal weight\n
    Also Provide all tickers in current universe
    '''
    m = no_of_stocks
    x = stocks_to_axe
    df = data.copy()
    portfolio = []
    monthly_ret = [0]

    for i in range(1, len(df)) :
        if len(portfolio) > 0 :
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        if include_portfolio_stocks :
            new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        else :
            new_picks = df[[t for t in tickers if t not in portfolio]].iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])

    try:
        return monthly_ret_df
    finally:
        monthly_ret_df = pd.DataFrame()
        df = pd.DataFrame()


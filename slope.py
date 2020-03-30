import pandas as pd
import numpy as np
import statsmodels.api as sm

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
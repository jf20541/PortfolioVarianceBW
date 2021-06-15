import pandas as pd
import config
from sklearn.linear_model import LinearRegression
import numpy as np 

# def factor_exposure(pca, beta_idx, beta_cols):
#     return pd.DataFrame(pca.components_.T, beta_idx, beta_cols)

def factor_returns(data):
    factor_1 = data.mean()
    factor_2 = data.mean()
    data['factor_1'] = factor_1 
    data['factor_2'] = factor_1 
    return pd.DataFrame(factor_1, factor_2)

# def factor_exposure(data, returns):
#     lr = LinearRegression()
#     X = np.array().T
#     print(X)
        # y = np.array(returns.values)
        # # lr.fit(X,y)
        # return lr.coef_

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()
    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()

    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi  

if __name__ == '__main__':
    df = pd.read_csv(config.TRAINING_FILE)
    print(computeRSI(df, 14))


# factor_return_1 = returns_df.mean(axis=1)
# factor_return_2 = returns_df.median(axis=1)
# factor_return_l = [factor_return_1, factor_return_2]
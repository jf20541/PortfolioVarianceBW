import pandas as pd
import config
from sklearn.linear_model import LinearRegression
import numpy as np 

class VarianceModel():
    def __init__(self, timeseries):
        self.timeseries = timeseries

    def factor_returns(self):
        factor_1 = self.timeseries.mean(axis=1)
        factor_2 = self.timeseries.median(axis=1)
        return [factor_1, factor_2]

    def factor_exposure(self, factor_return_l, asset_return):
        lr = LinearRegression()
        X = np.array(factor_return_l).T
        y = np.array(asset_return.values)
        lr.fit(X,y)
        return lr.coef_

    def exposure(self):
        factor_exposure_l = []
        for i in range(len(self.timeseries.columns)):
            factor_exposure_l.append(
                self.factor_exposure(self.factor_returns(),
                                    self.timeseries[self.timeseries.columns[i]]
                                    ))
            
        factor_exposure_a = np.array(factor_exposure_l)
        print(factor_exposure_a)
        print(f"factor_exposures for asset # {factor_exposure_a[0]}")




if __name__ == '__main__':
    df = pd.read_csv(config.TRAINING_FILE)
    var = VarianceModel(df)
    print(var.exposure())
    
    # factor_return_1 = df.mean(axis=1)
    # print(factor_return_1)
    # factor_return_2 = df.median(axis=1)
    # print(factor_return_2)
















# class Variance():
#     def __init__(self, timeseries):
#         self.timeseries = timeseries

#     def factor_returns(self):
#         factor_1 = self.timeseries.mean(axis=1)
#         factor_2 = self.timeseries.median(axis=1)
#         return pd.DataFrame(factor_1, factor_2)

# def factor_returns(returns, return_idx, return_cols):
#     return pd.DataFrame(returns, return_idx, return_cols)

# def factor_exposure(beta_idx, beta_cols):
#     return pd.DataFrame(beta_idx, beta_cols)



# class VarianceModel:
#     def __init__(self, returns):
#         self.factor_exposure_ = factor_exposure(returns.columns.values, returns.shape[1])
#         self.factor_returns_ = factor_returns(returns, returns.index, returns.shape[1])
        # self.factor_cov_matrix_ = factor_cov_matrix(self.factor_returns_, ann_factor)
        # self.idiosyncratic_var_matrix_ = idiosyncratic_var_matrix(returns, self.factor_returns_, self.factor_exposure_, ann_factor)
    # pca_model = PCARiskModel(returns, 252, 4, pca)

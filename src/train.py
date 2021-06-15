import pandas as pd
import config
from sklearn.linear_model import LinearRegression
import numpy as np 

class VarianceModel():
    def __init__(self, timeseries):
        self.timeseries = timeseries

    def factors(self):
        factor_1 = self.timeseries.mean(axis=1)
        factor_2 = self.timeseries.median(axis=1)
        return [factor_1, factor_2]

    def factor_exposure(self, factor_return, asset_return):
        lr = LinearRegression()
        X = np.array(factor_return).T
        y = np.array(asset_return.values)
        lr.fit(X,y)
        return lr.coef_

    def exposure(self):
        all_exposure = []
        for i in range(len(self.timeseries.columns)):
            all_exposure.append(
                self.factor_exposure(self.factors(),
                                    self.timeseries[self.timeseries.columns[i]]
                                    ))
            
        factor_exposure_a = np.array(all_exposure)
        # print(factor_exposure_a)
        # print(f"factor_exposures for asset {factor_exposure_a[0]}")

        return factor_exposure_a

    def var_returns(self):
        return np.var(self.timeseries)
    
    def comm_var(self):
        factor_exposure_1_1 = self.exposure()[0][0]
        factor_exposure_1_2 = self.exposure()[0][1]
        common_return_1 = factor_exposure_1_1 * self.factors()[0]+ factor_exposure_1_2 * self.factors()[1]
        specific_return_1 = self.timeseries['SPY'] - common_return_1
        return specific_return_1

    def cov(self):
        covm_f1_f2 = np.cov(factor_return_1,factor_return_2,ddof=1) #this calculates a covariance matrix
        # TODO: get the variance of each factor, and covariances from the covariance matrix covm_f1_f2
        var_f1 = covm_f1_f2[0,0]
        var_f2 = covm_f1_f2[1,1]
        cov_f1_f2 = covm_f1_f2[0][1]

        # TODO: calculate the specific variance.  
        var_s_1 = np.var(specific_return_1,ddof=1)

        # TODO: calculate the variance of asset 1 in terms of the factors and specific variance
        var_asset_1 = (factor_exposure_1_1**2 * var_f1) + \
                    (factor_exposure_1_2**2 * var_f2) + \
                    2 * (factor_exposure_1_1 * factor_exposure_1_2 * cov_f1_f2) + \
                    var_s_1
        print(f"variance of asset 1: {var_asset_1:.8f}")

if __name__ == '__main__':
    df = pd.read_csv(config.TRAINING_FILE)
    var = VarianceModel(df)
    # print(var.exposure())
    # print(var.var_returns())
    print(var.comm_var())
    # print(var.main())
    
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

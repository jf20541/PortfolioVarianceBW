import pandas as pd
import config
from sklearn.linear_model import LinearRegression
import numpy as np


class VarianceModel:
    def __init__(self, timeseries):
        self.timeseries = timeseries

    def factors(self):
        factor_1 = self.timeseries.mean(axis=1)
        factor_2 = self.timeseries.median(axis=1)
        return factor_1, factor_2

    def factor_exposure(self, factor_return, asset_return):
        lr = LinearRegression()
        X = np.array(factor_return).T
        y = np.array(asset_return.values)
        lr.fit(X, y)
        return lr.coef_

    def exposure(self):
        all_exposure = []
        for i in range(len(self.timeseries.columns)):
            all_exposure.append(
                self.factor_exposure(
                    self.factors(), self.timeseries[self.timeseries.columns[i]]
                )
            )

        factor_exposure_a = np.array(all_exposure)
        return factor_exposure_a

    def comm_var(self):
        factor_exposure_1_1 = self.exposure()[0][0]
        factor_exposure_1_2 = self.exposure()[0][1]
        common_return_1 = (
            factor_exposure_1_1 * self.factors()[0]
            + factor_exposure_1_2 * self.factors()[1]
        )
        specific_return_1 = self.timeseries["AAPL"] - common_return_1
        return [
            factor_exposure_1_1,
            factor_exposure_1_2,
            common_return_1,
            specific_return_1,
        ]

    def cov(self):
        covm_f1_f2 = np.cov(self.factors()[0], self.factors()[1], ddof=1)
        var_f1 = covm_f1_f2[0, 0]
        var_f2 = covm_f1_f2[1, 1]
        cov_f1_f2 = covm_f1_f2[0][1]

        var_s_1 = np.var(self.comm_var()[3], ddof=1)

        var_asset_1 = (
            (self.comm_var()[0] ** 2 * var_f1)
            + (self.comm_var()[1] ** 2 * var_f2)
            + 2 * (self.comm_var()[0] * self.comm_var()[1] * cov_f1_f2)
            + var_s_1
        )
        print(f"variance of asset 1: {var_asset_1:.8f}")


if __name__ == "__main__":
    df = pd.read_csv(config.TRAINING_FILE)
    var = VarianceModel(df)
    print(var.exposure())
    # print(var.var_returns())
    # print(var.comm_var())
    print(var.cov())

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

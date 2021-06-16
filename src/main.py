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

    def variance(self):
        return np.array(np.var(self.timeseries))

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

    def factor_covariance(self):
        return np.cov(self.factors()[0], self.factors()[1], ddof=1)

    def weights(self):
        return np.full([10, 1], 0.10)

    def asset_weights(self, asset_weights):
        weights = np.array(asset_weights)
        rebalance_weights = weights / np.sum(weights)
        return rebalance_weights


if __name__ == "__main__":
    df = pd.read_csv(config.TRAINING_FILE)
    model = VarianceModel(df)
    B = model.exposure()
    F = model.factor_covariance()
    S = np.diag(model.variance())
    X = model.asset_weights(config.WEIGHTS)
    var_portfolio = X.T.dot(B.dot(F).dot(B.T) + S).dot(X)
    print(f"Bridgewater Associates Portfolio Variance is {var_portfolio:.8f}")

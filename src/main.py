import pandas as pd
import config
from sklearn.linear_model import LinearRegression
import numpy as np


class VarianceModel:
    def __init__(self, timeseries):
        self.timeseries = timeseries

    def factors(self):
        """
        Returns: calculated median and mean factor as float
        """
        factor_1 = self.timeseries.mean(axis=1)
        factor_2 = self.timeseries.median(axis=1)
        return factor_1, factor_2

    def idiosyncratic_variance(self):
        """
        Returns: numpy array of returns variance as float
        """
        return np.var(self.timeseries)

    def factor_exposure(self, factor_return, asset_return):
        """
        Parameters
        -----------
        factor_return: calculate the exposed of each asset to each factor, float
        asset_return: daily returns from time-series
        --------
        Returns: coefficient as float
        """
        lr = LinearRegression()
        X = np.array(factor_return).T
        y = np.array(asset_return.values)
        lr.fit(X, y)
        return lr.coef_

    def exposure(self):
        """
        Returns: array-like of collected all assets exposures
        """
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
        """
        Returns: array-like of factor covariance
        """
        return np.cov(self.factors()[0], self.factors()[1], ddof=1)

    def asset_weights(self, asset_weights):
        """
        Parameters
        -----------
        asset_weights: array-like for asset's respective weights
        --------
        Returns: rebalanced weights so sum equal to 100
        """
        weights = np.array(asset_weights)
        rebalance_weights = weights / np.sum(weights)
        return rebalance_weights


if __name__ == "__main__":
    df = pd.read_csv(config.TRAINING_FILE)
    model = VarianceModel(df)
    B = model.exposure()
    F = model.factor_covariance()
    S = np.diag(model.idiosyncratic_variance())
    X = model.asset_weights(config.WEIGHTS)
    var_portfolio = X.T.dot(B.dot(F).dot(B.T) + S).dot(X)
    print(f"Bridgewater Associates Portfolio Variance is {var_portfolio:.8f}")

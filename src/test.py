import config
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def factor_exposure(pca, beta_idx, beta_cols):
    """
    Parameters
    - pca: dimensionality reduction
    - beta_idx: 1 dimensional np-array containing index-dates
    - beta_cols: 1 dimensional np-array of (n_components - 1)

    Returns: Pandas DataFrame of Factor Exposure (B)
    """
    return pd.DataFrame(pca.components_.T, beta_idx, beta_cols)


def factor_returns(pca, returns, return_idx, return_cols):
    """
    Parameters
    - pca: dimensionality reduction
    - returns: daily returns dataframe
    - return_idx: dimensional np-array containing index-dates
    - return_cols: 1 dimensional np-array of (n_components - 1)

    Returns: Pandas DataFrame of Factor Returns (f)
    """
    return pd.DataFrame(pca.transform(returns), return_idx, return_cols)


def idiosyncratic_var_matrix(returns, factor_returns, factor_exposure, ann_factor):
    """
    Parameters
    - returns: daily returns dataframe
    - factor_returns: output of the factor_returns function
    - factor_exposure: output of the factor_exposure function
    - ann_factor: annualized of 252 trading days

    Returns: Pandas DataFrame of Idiosyncratic Risk (s)
    """
    common_returns = pd.DataFrame(
        np.dot(factor_returns, factor_exposure.T), returns.index, returns.columns
    )
    residuals = returns - common_returns
    return pd.DataFrame(
        np.diag(np.var(residuals)) * ann_factor, returns.columns, returns.columns
    )


def factor_cov_matrix(factor_returns, ann_factor):
    """
    Parameters
    - factor_returns: output of the factor_exposure function
    - ann_factor: annualized of 252 trading days

    Returns: calculated the annualized factor covariance in diagonal np-array
    """
    return np.diag(factor_returns.var(axis=0, ddof=1) * ann_factor)


class PCARiskModel:
    """
    Parameters
    - returns: daily returns dataframe
    - ann_factor: annualized of 252 trading days
    - n_components: number of PC
    - pca: dimensionality reduction

    Returns: returns time-series
    """

    def __init__(self, returns, ann_factor, n_components, pca):
        self.factor_exposure_ = factor_exposure(
            pca, returns.columns.values, np.arange(n_components)
        )
        self.factor_returns_ = factor_returns(
            pca, returns, returns.index, np.arange(n_components)
        )
        self.factor_cov_matrix_ = factor_cov_matrix(self.factor_returns_, ann_factor)
        self.idiosyncratic_var_matrix_ = idiosyncratic_var_matrix(
            returns, self.factor_returns_, self.factor_exposure_, ann_factor
        )


if __name__ == "__main__":
    returns = pd.read_csv(config.TRAINING_FILE)

    # initiate PCA and fit daily returns
    pca = PCA(n_components=4, svd_solver="full")
    pca.fit(returns)

    # Call the PCARiskModel class to plot 4 component returns
    pca_model = PCARiskModel(returns, 252, 4, pca)

    for idx, val in enumerate(pca.explained_variance_ratio_):
        print(f"Principal Component  {idx} for {val}")

    # plot Total Percent Variance Explained and Factor Returns
    def plot():
        plt.bar(np.arange(4), pca.explained_variance_ratio_)
        plt.title("Total Percent Variance Explained")
        plt.ylabel("Explained Variance (%)")
        plt.xlabel("Number of Components")
        plt.savefig("../plots/TotalPCA.png")

        pca_model.factor_returns_.loc[:, 0:3].cumsum().plot()
        plt.title("Factor Returns")
        plt.ylabel("Component Returns(%)")
        plt.xlabel("Time")
        plt.savefig("../plots/Factor Returns.png")

    plot()
    plt.show()

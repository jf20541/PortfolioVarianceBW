import pandas as pd
import yfinance as yf
import numpy as np

if __name__ == "__main__":
    """
    Collect Bridgewater top 25 holdings Adj-Closing Price
    Calculate returns, clean data and save to CSV file
    """
    assets = "SPY VWO WMT PG BABA KO JNJ GLD PEP IEMG MCD COST FXI IVV SBUX PDD MCHI IAU LQD EL ABT TGT MDLZ JD DHR"
    df = yf.download(assets, start="2020-01-06", end="2021-01-06")
    df = df["Adj Close"]
    df = df.apply(lambda x: x - (x.shift(1)))[1:] / 100
    df.to_csv("../inputs/train.csv", index_label=False)
    if df.isnull().values.any() == False:
        print("Data is Clean")
    else:
        print("Found Null Values")

import pandas as pd
import yfinance as yf

if __name__ == "__main__":
    df = yf.download(
        "SPY VWO WMT PG BABA KO JNJ GLD PEP IEMG", start="2020-01-01", end="2021-01-01"
    )
    df = df["Adj Close"]
    df = df.apply(lambda x: x - (x.shift(1)))[1:]
    df.to_csv("../inputs/train.csv", index_label=False)
    # "SPY VWO WMT PG BABA KO JNJ GLD PEP IEMG"
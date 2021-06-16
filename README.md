# PortfolioVarianceBW

## Goal
Calculated the top 25 holdings(%) total risk inherent for Bridgewater Associated\
Calculating the squared weights mutiplied by each asset's variance plus the covariance of the universe assets multipled by its weights

## Metric
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20%5CLARGE%20Portfolio%20Variance%20%3D%20%5Cmathbf%7BW%5E%7BT%7D%28BFB%5E%7BT%7D&plus;%20S%29W%7D)
\

Array of factors covariance\
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20%5CLARGE%20%5Cmathbf%7BF%7D%20%3D%20%5Cbigl%28%5Cbegin%7Bsmallmatrix%7D%20Var%28f_%7B1%7D%29%20%26%20Cov%28f_%7B1%7D%2C%20f_%7Bn%7D%29%5C%5C%20Cov%28f_%7Bn%7D%2C%20f_%7B1%7D%20%26%20Var%28f_%7Bn%7D%29%20%5Cend%7Bsmallmatrix%7D%5Cbigr%29)


Array of factor exposures\
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20%5CLARGE%20%5Cmathbf%7BB%5Cemph%7B%7D%7D%20%3D%20%5Cbigl%28%5Cbegin%7Bsmallmatrix%7D%20%5Cbeta%20_%7B1%2C1%7D%2C%20%26%20%5Cbeta%20_%7B1%2Cn%7D%5C%5C%20%5Cbeta%20_%7Bn%2C1%7D%2C%20%26%20%5Cbeta%20_%7Bn%2Cn%7D%20%5Cend%7Bsmallmatrix%7D%5Cbigr%29)


Array of idiosyncratic variances\
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20%5CLARGE%20%5Cmathbf%7BS%7D%20%3D%20%5Cbigl%28%5Cbegin%7Bsmallmatrix%7D%20Var%28s_%7Bi%7D%29%20%26%200%5C%5C%200%20%26%20Var%28s_%7Bj%7D%29%20%5Cend%7Bsmallmatrix%7D%5Cbigr%29)

Column vector for asset's weights\
![](https://latex.codecogs.com/gif.latex?%5Cdpi%7B120%7D%20%5CLARGE%20%5Cmathbf%7BW%7D%20%3D%20%5Cbinom%7Bw_%7B1%7D%7D%7Bw_%7Bn%7D%7D)

## Universe
[Bridgewater Associates's 13F Securities for Q12021](https://whalewisdom.com/filer/bridgewater-associates-inc#tabholdings_tab_link)\
SPY, VWO, WMT, PG, BABA, KO, JNJ, GLD, PEP, IEMG, MCD, COST, FXI, IVV, SBUX, PDD, MCHI, IAU, LQD, EL, ABT, TGT, MDLZ, JD, DHR



## Output
```bash
Bridgewater Associates Portfolio Variance is 0.00053133
```

### Code
Created 3 modules
- `config.py`: Define path as global variables
- `main.py`: Calculated the portolfio variance
- `data.py`: Collect the top 25 holdings concentration in BridgeWater Associates 13-F Filings as of 1Q2021

### Install
Install the following Python libraries
- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org)
- [YFinance](https://pypi.org/project/yfinance/)

### Run
In a terminal or command window, navigate to the top-level project directory `MonteCarloPorfolioOptimization/` (that contains this README) and run the following command:
```bash
pip install --upgrade pip && pip install -r requirements.txt
``` 

## Sources
https://whalewisdom.com/filer/bridgewater-associates-inc#tabholdings_tab_link

# USD-Libor-Yield-Curve-Modeling
Computational finance lab final project

## Summary
* [Project purpose](#abs-background-purpose)
* [Project structure](#project-structure)
* [Project implementation]((#abs-implementation))

### Project purpose
In this project, we create `USD LIBOR yield curve` model from market observations, via the methodology in use prior to 2008. It is to support two calculations:

1. The **discount factor** up to 3 years after a given spot date.
2. The **forward rate** which is the simple interest rate, expressed as a percentage, over a given period between two dates, computed from the above discount factor curve.

### Project structure 
This project consists of the following files:
#### Input files
* `depoRates.txt` - contains a series of annualized cash deposit rates. 
* `futuresPrices.txt` - contains a series of prices of Eurodollar futures, which are futures on 3 month cash LIBOR deposits.
* `tradeDate.txt` - contains the date at which the rates/prices are being observed, given as character strings in the form `YYYY-MM-DD`.
* `holidayCalendar.txt` - contains the dates of Federal Reserve holidays, given as character strings in the form `YYYY-MM-DD`, for the next five years (available from, among other places, the Federal Reserve website).

#### Class files

* `USDYieldCurve.py` - contains class to create USD yield curve object and compute *discound factor* and *forward rate*. 
* `USDYieldCurveDate.py` - contains class to compute all USD yeild curve related dates, e.g., *modified following date*, *spot date*. 
* `main.py` - contains the testing program.
* `YCtestcase.xlsm` - contains the testing case data. 

#### Project implementation
This project cound imprt into Python3 environment and run via the commends
```python
import USDYieldCurve
usdCurve = USDYieldCurve("depoRates.txt", "futuresPrices.txt", "tradeDate.txt", "holidayCalendar.txt")
print(usdCurve.getDfToDate(d1)) # d1 is a string in YYYY-MM-DD format
print usdCurve.getFwdRate(d2, d3) # inputs are in YYYY-MM-DD firnat
```














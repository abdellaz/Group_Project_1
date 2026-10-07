import yfinance as yf
import pandas as pd

tickers = ["MCD", "WING", "CAKE"]

start_date = "2026-07-01"
end_date = "2026-09-01"

data = yf.download(
    tickers,
    start=start_date,
    end=end_date
)

print(data.head())

print("\nDate Range:")
print(data.index.min(), "to", data.index.max())

print("\nNumber of Records:")
print(len(data))

print("\nColumn Names:")
print(data.columns)

print("\nData Types:")
print(data.dtypes)

print("\nMissing Values:")
print(data.isnull().sum())
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

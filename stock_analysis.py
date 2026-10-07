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

close_prices = data["Close"]

daily_returns = close_prices.pct_change() * 100

print("\nDaily Percentage Returns:")
print(daily_returns.head())

print("\nClosing Price Statistics:")

for ticker in tickers:
    print(f"\n{ticker}:")
    print("Count:", close_prices[ticker].count())
    print("Mean:", close_prices[ticker].mean())
    print("Median:", close_prices[ticker].median())
    print("Min:", close_prices[ticker].min())
    print("Max:", close_prices[ticker].max())
    print("Standard Deviation:", close_prices[ticker].std())

print("\nDaily Return Statistics:")

for ticker in tickers:
    print(f"\n{ticker}:")
    print("Count:", daily_returns[ticker].count())
    print("Mean:", daily_returns[ticker].mean())
    print("Median:", daily_returns[ticker].median())
    print("Min:", daily_returns[ticker].min())
    print("Max:", daily_returns[ticker].max())
    print("Standard Deviation:", daily_returns[ticker].std())

correlation_matrix = daily_returns.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

monthly_average = close_prices.resample("ME").mean()

print("\nMonthly Average Closing Prices:")
print(monthly_average)
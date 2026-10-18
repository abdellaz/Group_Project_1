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

mcd_returns = daily_returns["MCD"]  # McDonald

max_return_date = mcd_returns.idxmax()
max_return_value = mcd_returns.max()

min_return_date = mcd_returns.idxmin()
min_return_value = mcd_returns.min()

print("\nMcDonald's Significant Daily Movements:")
print("Largest Increase Date:", max_return_date)
print("Largest Increase Return:", max_return_value)

print("Largest Decrease Date:", min_return_date)
print("Largest Decrease Return:", min_return_value)

print("\nMcDonald's Data Around Q2 Earnings:")
print(data.loc["2026-08-03":"2026-08-07", [("Close", "MCD"), ("Volume", "MCD")]])

print("\nMcDonald's Returns Around Q2 Earnings:")
print(daily_returns.loc["2026-08-03":"2026-08-07", "MCD"])

wing_returns = daily_returns["WING"]  # Wingstop

max_return_date = wing_returns.idxmax()
max_return_value = wing_returns.max()

min_return_date = wing_returns.idxmin()
min_return_value = wing_returns.min()

print("\nWingstop's Significant Daily Movements:")
print("Largest Increase Date:", max_return_date)
print("Largest Increase Return:", max_return_value)

print("Largest Decrease Date:", min_return_date)
print("Largest Decrease Return:", min_return_value)

print("\nWingstop's Data Around Q2 Earnings:")
print(data.loc["2026-08-02":"2026-08-07", [("Close", "WING"), ("Volume", "WING")]])

print("\nWingstop's Returns Around Q2 Earnings:")
print(daily_returns.loc["2026-08-02":"2026-08-07", "WING"])

from pathlib import Path

import pandas as pd
import yfinance as yf

# Cheesecake Factory stock ticker from the beginning of July 2026 through the end of August 2026.
TICKERS = ["CAKE"]
START_DATE = "2026-07-01"
END_DATE = "2026-09-01"

# Using Yahoo Finance to download data for the Cheesecake Factory stock ticker from the beginning 
# of July 2026 through the end of August 2026. Including high, low, open and close prices as well as volume.
raw = yf.download(
    TICKERS,
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True,
    progress=False,
)
if raw is None or raw.empty:
    raise RuntimeError("No rows returned. Check the internet connection, tickers, and dates.")

print("Requested dates:", START_DATE, "through", END_DATE)
print("Shape:", raw.shape)
print("Columns:")
print(raw.columns)
print("Data types:")
print(raw.dtypes)
print("Missing values:")
print(raw.isna().sum())
print(raw)

long = raw.stack(level="Ticker", future_stack=True).rename_axis(["Date", "Ticker"]).reset_index()
long["Date"] = pd.to_datetime(long["Date"])
long = long.sort_values(["Ticker", "Date"]).reset_index(drop=True)
prices = long

# Count, mean, median, min, max, std for closing price and daily
prices["Daily_Return_Pct"] = prices.groupby("Ticker")["Close"].pct_change() * 100

required_stats = ["count", "mean", "median", "min", "max", "std"]
stats = prices.groupby("Ticker")[["Close", "Daily_Return_Pct"]].agg(required_stats)
print("\nDescriptive statistics (Close in dollars, Daily_Return_Pct in percent):")
print(stats)

return_matrix = prices.pivot(index="Date", columns="Ticker", values="Daily_Return_Pct")
correlation_matrix = return_matrix.corr()
print("\nCorrelation matrix of daily returns:")
print(correlation_matrix)

# Summary statistics for July and August
monthly_summary = (
    prices.assign(Month=prices["Date"].dt.to_period("M").dt.to_timestamp())
    .groupby(["Month", "Ticker"], as_index=False)["Close"]
    .mean()
    .rename(columns={"Close": "Average_Close"})
)
print("\nMonthly average close:")
print(monthly_summary)

# Highest return and lowest return days
print("\nSignificant movements:")
for ticker, ticker_data in prices.groupby("Ticker"):
    highest_return = ticker_data.sort_values("Daily_Return_Pct", ascending=False).iloc[0]
    lowest_return = ticker_data.sort_values("Daily_Return_Pct", ascending=True).iloc[0]

    print(ticker)
    print("Highest return:")
    print(highest_return)
    print("Lowest return:")
    print(lowest_return)

Path("outputs").mkdir(exist_ok=True)
stats.to_csv("outputs/descriptive_statistics.csv")
correlation_matrix.to_csv("outputs/correlation_matrix.csv")
monthly_summary.to_csv("outputs/monthly_summary.csv", index=False)


##chart 1: Full-Period Normalized Price Comparison
import matplotlib.pyplot as plt
normalized = close_prices.div(close_prices.iloc[0]).mul(100)
normalized.plot(figsize=(10, 6))
plt.title("Normalized price performance across the analysis period")
plt.xlabel("Date")
plt.ylabel("Indexed price (first observation = 100)")
plt.tight_layout()
plt.savefig("charts/normalized_prices.png", dpi=150)
plt.show()

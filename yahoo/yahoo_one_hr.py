import yfinance as yf
import pandas as pd

ticker = "NQ=F"
#data = yf.download(tickers = ticker, start='2010-01-04', end='2018-12-31')
data = yf.download(tickers = ticker, period = "2mo", interval = '5m')
# data = yf.download(tickers = ticker, start='2017-01-04', end='2018-12-31', interval = '5m')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# https://pypi.org/project/yfinance/
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

# print(df1)

df = df1.reset_index()

# print(df)

df7 = df.rename(columns = {'Date': 'date', 'Open':'open', 'High': 'high', 'Low':'low', 'Close':'close','Volume': 'volume'}, inplace = False)

print(df7)
df7.to_csv('daily.csv')

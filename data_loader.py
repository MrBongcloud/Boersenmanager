import yfinance as yf
import os

foldername = 'Shares'
os.makedirs(foldername, exist_ok = True)


stocks = ['AAPL','NVDA', 'GOOG', 'META', 'TSLA', 'BAS.DE']

for stock in stocks:
    data = yf.download(stock, start="2026-04-01")
    data.to_csv(os.path.join(foldername, f"{stock}.csv"))
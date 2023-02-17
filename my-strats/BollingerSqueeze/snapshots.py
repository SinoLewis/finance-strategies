import yfinance as yf

with open('S&P500.csv') as f:
    stocks = f.read().splitlines()
    for symbol in stocks:
        data = yf.download(symbol, start='2021-05-01', end='2021-06-30')
        with open(f"DataSets\{symbol}.csv", "w") as f:
            data.to_csv(f)
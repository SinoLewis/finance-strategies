import os
import plotly.graph_objects as go
import pandas as pd

for filename in os.listdir('DataSets'):
    symbols = ['AAPL', 'TSLA']
    try:
        symbol = filename.split('.')[0]
        df = pd.read_csv(f'Datasets\{symbol}.csv')
        if df.empty:
            continue
        
        df['20sma'] = df['Close'].rolling(window=20).mean()
        df['stdev'] = df['Close'].rolling(window=20).std()
        df['upperbound'] = df['20sma'] + (2 * df['stdev'])
        df['lowerbound'] = df['20sma'] - (2 * df['stdev'])
        
        if symbol in symbols:
            print(df)
            candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
            upper_bands = go.Scatter(x=df['Date'], y=df['upperbound'], name='Upper Bollinger Band')
            lower_bands = go.Scatter(x=df['Date'], y=df['lowerbound'], name='Lower Bollinger Band')
            fig = go.Figure(data=[candlestick, upper_bands, lower_bands])

            fig.show()
    except FileNotFoundError as e:
        print(e)
        continue
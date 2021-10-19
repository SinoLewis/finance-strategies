import ccxt, json, os
import pandas_ta as ta
import requests, time
import pandas as pd
pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime

exchange  = ccxt.binance()

def check_adx():
    bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=1500)
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    adx = df.ta.adx()
    df = pd.concat([df, adx], axis=1)
    last_row = df.iloc[-1]
    in_position = False
    data = None

    if last_row['ADX_14'] >= 25:
        if last_row['DMP_14'] > last_row['DMN_14']:
            message = f"SRONG UPTREND: ADX is {last_row['ADX_14']:.2f}\nDMP & DMN is {last_row['DMP_14']:.2f}, {last_row['DMN_14']:.2f}"
            print(message)
            if in_position == False:
                data = {
                        'ticker':'ETH/USDT',
                        'type': 'buy',
                        'in_postion': True,
                        'stake': 0.05,
                        'price': last_row['close'],
                    }
                #with open('.\\trades.json', 'a') as f:
                #    json.dump(data, f, indent=2)
                in_position = True
        if last_row['DMP_14'] < last_row['DMN_14']:    
            message = f"SRONG DOWNTREND: ADX is {last_row['ADX_14']:.2f}\nDMP & DMN is {last_row['DMP_14']:.2f}, {last_row['DMN_14']:.2f}"
            print(message)
            if in_position == True:
                data = {
                        'ticker':'ETH/USDT',
                        'type': 'sell',
                        'in_postion': False,
                        'stake': 0.05,
                        'price': last_row['close'],
                    }
                #with open('.\\trades.json', 'a') as f:
                #    json.dump(data, f, indent=2)
                in_position = False
    if last_row['ADX_14'] < 25:
        message = f"NO TREND: ADX is {last_row['ADX_14']:.2f} \nDMP & DMN is {last_row['DMP_14']:.2f}, {last_row['DMN_14']:.2f}"
        print(message)
        if in_position == True:
            data = {
                'ticker':'ETH/USDT',
                'type': 'sell',
                'stake': 0.05,
                'in_postion': False,
                'price': df['close'][last_row_index]
                }
            #with open('.\\trades.json', 'a') as f:
            #    json.dump(data, f, indent=2)
            in_position = False
    payload = {
            'username': 'ADX ETH/USDT',
            'content': f'{message}\nTrade: {data}\nIn Postion: {in_position}'
        }
    return payload, df.tail(5)
def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr

def supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
        
    return df


in_position = False

def check_buy_sell_signals(df):
    global in_position

    print("checking for buy and sell signals")
    print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    data = None

    if df['in_uptrend'][previous_row_index] == False and df['in_uptrend'][last_row_index] == True:
        print("changed to uptrend, buy")
        if in_position == False:
            #order = exchange.create_market_buy_order('ETH/USD', 0.05)
            #print(order)
            data = {
                'ticker':'ETH/USDT',
                'type': 'buy',
                'stake': 0.05,
                'in_postion': True,
                'price': df['close'][last_row_index]
                }
            #with open('.\\trades.json', 'a') as f:
            #    json.dump(data, f, indent=2)
            in_position = True
        else:
            print("already in position, nothing to do")
    
    if df['in_uptrend'][previous_row_index] == True and df['in_uptrend'][last_row_index] == False:
        print("changed to downtrend, sell")
        if in_position == True:
            #order = exchange.create_market_sell_order('ETH/USD', 0.05)
            #print(order)
            data = {
                'ticker':'ETH/USDT',
                'type': 'sell',
                'stake': 0.05,
                'in_postion': False,
                'price': df['close'][last_row_index]
                }
            #with open('.\\trades.json', 'a') as f:
            #    json.dump(data, f, indent=2)
            in_position = False
        else:
            print("You aren't in position, nothing to sell")

    payload = {
        'username': 'SuperTrend',
        'content': f"Uptrend: {df['in_uptrend'][last_row_index]}\nClose: {df['close'][last_row_index]}\nTrade:{data}\nIn Postion: {in_position}"
    }
    return payload

def run_bot():
    print(f"Fetching new bars for {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
    bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=900)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    supertrend_data = supertrend(df)
    
    payload = check_buy_sell_signals(supertrend_data)
    return payload

while True:
    try:
        # ADX
        payload, data = check_adx()
        requests.post(os.environ['DISCORD_FINANCE_WEBHOOK'], json=payload)
        print(data)
        # SuperTrend
        payload_2 = run_bot()
        requests.post(os.environ['DISCORD_FINANCE_WEBHOOK'], json=payload_2)
    except Exception as e:
        print(e)
    time.sleep(60)
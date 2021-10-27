# py-finance-startegies
Analysis of various Finicial Strategy indicators
This is a Discord notification app that tracks our Strategies After every 5min

Requirements:
- ccxt lib generates our candle-sticks date-time series data from binance crypto market
- 2 main Strategies:  adx & supertrend which will be send as a notification considering its postion on the candlestick
- Final main logic

ALGO
1. check_adx - 
2. tr, atr, supertrend - used to find super-trend on the indicators
3. check_buy_signals - takes adx & super-trend and determines the postion which should be held
4. run_bot  - runs the perpertual data request from  ccxt & populates the date-time series data
            - it then runs the data through the check_buy_signal and returns a json data that will be send as a notification to discord
5. main logic   - an infinite loop that runs code then sleep for 60 seconds
                - runs adx logic the, sends adx to discord, prints adx dataframe
                - runs supertrend, sends supertrend data to discord
                ENDS

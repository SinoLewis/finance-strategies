from pprint import pprint
import time, os, requests, json, sys
import urllib.parse
import hashlib
import hmac
import base64
from config import *

sys.path.insert(0, '/home/samespoil/HackersLounge/RealTime/')
# from bot import * 

#Kraken Private Api Auth
api_url = "https://api.kraken.com"    
def get_kraken_signature(urlpath, data, secret):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()
# Default private Api request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

def iskrakenUp():
    # Check if the Kraken is on
    resp = requests.get('https://api.kraken.com/0/public/SystemStatus')
    data = resp.json()
    return data['result'] if data['error'] == [] else 'OFFLINE'

def getMarketPrice():
    resp = requests.get("https://api.kraken.com/0/public/OHLC?pair=XBTUSD&intervel=60")
    return resp.json()
    # If market price has been updated in the file return updated file
    # else return current price QueryOrders

# To confirm operations made by the bot
def getOperationalDetails(operationId):
    return 

isNextOperationBuy = True

UPWARD_TREND_THRESHOLD = 1.5
DIP_THRESHOLD = -2.25

PROFIT_THRESHOLD = 1.25
STOP_LOSS_THRESHOLD = -2.00

lastOpPrice = 100

# Operation of Orders
params = {
    'BuyLimitOrder':{
        "nonce": str(int(1000*time.time())),
        "ordertype": "limit",
        "type": "buy",
        "volume": 1.25,
        "pair": "XBTUSD",
        "price": 27500
    },
    'BuyMarketOrder':{
        "nonce": str(int(1000*time.time())),
        "ordertype": "limit",
        "type": "buy",
        "volume": 1.25,
        "pair": "XBTUSD",
        "price": 27500
    },
    'SellLimitOrder':{
        "nonce": str(int(1000*time.time())),
        "ordertype": "limit",
        "type": "sell",
        "volume": 1.25,
        "pair": "XBTUSD",
        "price": 27500
    },
    'SellMarketOrder':{
        "nonce": str(int(1000*time.time())),
        "ordertype": "limit",
        "type": "sell",
        "volume": 1.25,
        "pair": "XBTUSD",
        "price": 27500
    },
    'CancelOrder':{
        "nonce": str(int(1000*time.time())),
        "txid": "OG5V2Y-RYKVL-DT3V3B"
    }}
def attemptToMakeTrade():
    currentPrice = float(getMarketPrice())
    pctDiff = (currentPrice - lastOpPrice)/lastOpPrice*100
    if isNextOperationBuy:
        tryToBuy(pctDiff)   
    else:
        tryToSell(pctDiff)

def tryToBuy(pctDiff):
    if pctDiff >= UPWARD_TREND_THRESHOLD or pctDiff <= DIP_THRESHOLD:
        lastOpPrice = kraken_request(api_url, params['BuyLimitOrder'], api_key, api_sec)
        isNextOperationBuy = False

def tryToSell(pctDiff):
    if pctDiff >= PROFIT_THRESHOLD or pctDiff <= STOP_LOSS_THRESHOLD:
        lastOpPrice = kraken_request(api_url, params['SellLimitOrder'], api_key, api_sec)
        isNextOperationBuy = True

if __name__ == '__main__':
    r = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    print(json.loads(r.text)['result'])
    # ORDER book
        # MARKET order
          # STOP market order; preventing loss
        # LIMIT order
          # OPEN Orders
            # SPREAD
            # BUY COIN at market PRICE

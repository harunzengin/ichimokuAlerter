import requests
import time
from app import ichimokuCalculator
import asyncio
from aiohttp import ClientSession
import json
keys = json.load(open("apiKeys.json"))
apiKey = keys["apiKey"]
secretKey = keys["secretKey"]
headers={'apiKey':apiKey,'secretKey': secretKey}
binance_base_url = "https://api.binance.com"
binance_ticker_url = binance_base_url + "/api/v3/ticker/price"
binance_time_response = requests.get(binance_base_url + "/api/v1/time")
server_time = int(round(time.time() * 1000))
binance_time = binance_time_response.json()["serverTime"]

exchange_response = requests.get(binance_base_url + "/api/v1/exchangeInfo")
if(exchange_response.status_code != 200):
    print("Could not get exchanges, The response is:")
    print(exchange_response.text)

exchange_rate_limits = exchange_response.json()["rateLimits"]
exchange_symbols_from_response = exchange_response.json()["symbols"]
exchange_symbols = []


def getTimeDifference():
    return (server_time - binance_time)

#initialize exchange symbols here
def initialize(icihimokuParams):
    oneHour = {}
    fourHours = {}
    oneDay = {}
    for i in range(len(exchange_symbols_from_response)):
        #print(exchange_symbols_from_response[i]['symbol'])
        currentSymbol = exchange_symbols_from_response[i]['symbol']
        oneHour[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol,'binance',icihimokuParams,'h')
        fourHours[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol, 'binance', icihimokuParams,'q')
        oneDay[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol, 'binance', icihimokuParams,'d')
    return (oneHour,fourHours,oneDay)


async def fetch(url, session,params):
    async with session.get(url, params=params, verify_ssl=False) as response:
        return await response.json()


async def runKlines(interval,maxparam):
    tasks = []
    klinesUrl = "https://api.binance.com/api/v1/klines"
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for symbol in exchange_symbols_from_response:
            currentSymbol = symbol['symbol']
            params = {"symbol": currentSymbol, "interval": interval, "limit":maxparam}
            task = asyncio.ensure_future(fetch(klinesUrl, session, params))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
    return responses

def getData(ichimokuParams,interval):
    maxparam = max(ichimokuParams)
    binanceinterval = str
    if (interval == 'h'):
        binanceinterval = '1h'
    if (interval == 'q'):
        binanceinterval = '4h'
    if (interval == 'd'):
        binanceinterval = '1d'
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(runKlines(binanceinterval,maxparam))
    responses = loop.run_until_complete(future)
    returndict = {}
    for i in range(len(exchange_symbols_from_response)):
        returndict[exchange_symbols_from_response[i]["symbol"]] = list(responses[i])
    return returndict

def getCurrentPrice():
    return requests.get(binance_ticker_url,headers=headers).json()
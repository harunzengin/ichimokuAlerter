import requests
import time as timer
from app import ichimokuCalculator
import asyncio
from aiohttp import ClientSession
import time
from datetime import datetime
market_url = "https://bittrex.com/api/v1.1/public/getmarkets"
markets = requests.get(market_url)
if(markets.status_code != 200):
    print("Could not get exchanges, The response is:")
    print(markets.text)
symbols = []
for symbol in markets.json()["result"]:
    symbols.append(symbol["MarketName"])
print(symbols)

market_summary = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ltc")
bittrex_time = market_summary.json()["result"][0]["TimeStamp"]
server_time = int(round(time.time() * 1000))
bittrex_time = int(datetime.strptime(bittrex_time,"%Y-%m-%dT%H:%M:%S.%f").timestamp() * 1000 )


def getTimeDifference():
    return (server_time - bittrex_time)


def initialize(ichimokuParams):
    oneHour = {}
    fourHours = {}
    oneDay = {}
    for currentSymbol in symbols:
        oneHour[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol, 'bittrex', ichimokuParams, 'h')
        fourHours[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol, 'bittrex', ichimokuParams, 'q')
        oneDay[currentSymbol] = \
            ichimokuCalculator.ichmimokuCalculator(currentSymbol, 'bittrex', ichimokuParams, 'd')
    return (oneHour, fourHours, oneDay)



async def fetch(url, session,params):
    async with session.get(url, params=params, verify_ssl=False) as response:
        if(response.status != 200):
            print(response.text)
            return fetch(url,session,params)
        return await response.json()


async def runKlines(interval,maxparam):
    tasks = []
    klinesUrl = "https://bittrex.com/Api/v2.0/pub/market/GetTicks"
    time = int(timer.time() * 1000)
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for symbol in symbols:
            currentSymbol = symbol
            params = {"marketName": currentSymbol, "tickInterval": interval, "_":time}
            task = asyncio.ensure_future(fetch(klinesUrl, session, params))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
    return responses


def getData(ichimokuParams,interval):
    maxparam = max(ichimokuParams)
    bittrexinterval = str
    if (interval == 'h'):
        bittrexinterval = 'hour'
    if (interval == 'd'):
        bittrexinterval = 'day'
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(runKlines(bittrexinterval,maxparam))
    responses = loop.run_until_complete(future)

    if (interval == 'd'):
        neccesaries = getNeccessaries(responses,maxparam)
        returndict = {}
        for i in range(len(symbols)):
            returndict[symbols[i]] = list(neccesaries[i])
        return returndict
    else:
        neccesariesday = getNeccessaries(responses,maxparam)
        returndictday = {}
        for i in range(len(symbols)):
            returndictday[symbols[i]] = list(neccesariesday[i])
        neccesariesquarter = getNecceariesquarterly(responses,maxparam)
        returndictquarter = {}
        for i in range(len(symbols)):
            returndictquarter[symbols[i]] = list(neccesariesquarter[i])
        return returndictday, returndictquarter


def getNeccessaries(responses,maxparam):
    returnlist = []
    for response in responses:
        response = response["result"]
        currentList = []
        for candle in response:
            currentList.append([float(candle["H"]),float(candle["L"])])
        returnlist.append(currentList[-maxparam:])
    return returnlist


def getNecceariesquarterly(responses,maxparam):
    returnlist = []
    for response in responses:
        response = response["result"]
        currentList = []
        while(response[0]["T"][11:]!= "00:00:00"):
            response.pop(0)
        subList = [response[n:n + 4] for n in range(0, len(response), 4)]
        for group in subList:
            highs = []
            lows = []
            for candle in group:
                highs.append(float(candle["H"]))
                lows.append(float(candle["L"]))
            currentList.append([max(highs), max(lows)])
        returnlist.append(currentList[-maxparam:])
    return returnlist


def getCurrentPrice():
    result = {}
    try:
        result = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")
    except requests.exceptions.SSLError:
        print("SSL Exception occured")
        return 0
    if result.status_code != 200:
        return 0
    else:
        return result.json()

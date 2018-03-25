from app import apiConnection
from app import timeManager
from app import ichimokuCalculator
import sys
import time
hour1,hour4,day1 = {},{},{}

def __main__():
    global hour1,hour4,day1
    ichimokuParams =[]
    timeDifference = apiConnection.getTimeDifference()
    if(len(sys.argv) == 1):
        ichimokuParams = [20,60,120,30]
    else:
        ichimokuParams = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
    print("Making initial API call with ichimoku params " + str(ichimokuParams))
    (hour1,hour4,day1) = apiConnection.initialize(ichimokuParams)
    print("Getting Kline Data")
    onehourdata = apiConnection.getData(ichimokuParams,'h')
    fourhourdata = apiConnection.getData(ichimokuParams,'q')
    onedaydata = apiConnection.getData(ichimokuParams,'d')
    print("Distributing initial data to calculator nodes")
    distribute_hourly_data(datadict=onehourdata)
    distribute_fourhour_data(datadict=fourhourdata)
    distribute_daily_data(datadict=onedaydata)
    print("Entering Loop")
    timeMgr = timeManager.timeManager(getTime() - timeDifference)
    while True:
        #get new klines after 10 seconds the server time update, to be sure
        action = timeMgr.getActionType(getTime() - 10000 - timeDifference)
        if(action == 'n'):
            current_Prices = apiConnection.getCurrentPrice()
            distribute_ticker_price(current_Prices)

        elif(action == 'h'):
            onehourdata = apiConnection.getData(ichimokuParams, 'h')
            distribute_hourly_data(datadict=onehourdata)
            print("renew hourly")

        elif(action == 'q'):
            fourhourdata = apiConnection.getData(ichimokuParams, 'q')
            distribute_fourhour_data(datadict=fourhourdata)
            print("renew quarterly")

        elif(action == 'd'):
            onedaydata = apiConnection.getData(ichimokuParams, 'd')
            distribute_daily_data(datadict=onedaydata)
            print("renew daily")

def distribute_hourly_data(datadict):
    for symbol in datadict:
        hour1[symbol].setInitialData(datadict[symbol])

def distribute_fourhour_data(datadict):
    for symbol in datadict:
        hour4[symbol].setInitialData(datadict[symbol])

def distribute_daily_data(datadict):
    for symbol in datadict:
        day1[symbol].setInitialData(datadict[symbol])

def distribute_ticker_price(pricedict):
    for symbol in pricedict:
        hour1[symbol['symbol']].calculateChange(float(symbol['price']))
        hour4[symbol['symbol']].calculateChange(float(symbol['price']))
        day1[symbol['symbol']].calculateChange(float(symbol['price']))

def getTime():
    return int(round(time.time() * 1000))

__main__()
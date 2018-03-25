from app import bittrexApiConnection
from app import timeManager
from app import ichimokuCalculator
import time
import sys

hour1,hour4,day1 = {},{},{}

def __main__():
    global hour1,hour4,day1
    ichimokuParams =[]
    if(len(sys.argv) == 1):
        ichimokuParams = [20,60,120,30]
    else:
        ichimokuParams = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
    print("Making initial API call with ichimoku params " + str(ichimokuParams))
    (hour1,hour4,day1) = bittrexApiConnection.initialize(ichimokuParams)
    print("Getting Kline Data")
    onehourdata, fourhourdata = bittrexApiConnection.getData(ichimokuParams,'h')
    onedaydata = bittrexApiConnection.getData(ichimokuParams,'d')
    print("Distributing initial data to calculator nodes")
    distribute_hourly_data(datadict=onehourdata)
    distribute_fourhour_data(datadict=fourhourdata)
    distribute_daily_data(datadict=onedaydata)
    print("Entering Loop")

    timeDifference = bittrexApiConnection.getTimeDifference()
    timeMgr = timeManager.timeManager(getTime() - timeDifference)

    while True:
        # get new klines after 10 seconds the server time update, to be sure
        action = timeMgr.getActionType(getTime() - 10000 - timeDifference)
        if action == 'n':
            current_Prices = bittrexApiConnection.getCurrentPrice()
            if current_Prices != 0:
                distribute_ticker_price(current_Prices)
        elif (action == 'h'):
            onehourdata = bittrexApiConnection.getData(ichimokuParams, 'h')[0]
            distribute_hourly_data(datadict=onehourdata)
            print("renew hourly")

        elif (action == 'q'):
            fourhourdata = bittrexApiConnection.getData(ichimokuParams, 'q')[1]
            distribute_fourhour_data(datadict=fourhourdata)
            print("renew quarterly")

        elif (action == 'd'):
            onedaydata =  bittrexApiConnection.getData(ichimokuParams, 'd')
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
    pricedict = pricedict["result"]
    for symbol in pricedict:
        hour1[symbol['MarketName']].calculateChange(float(symbol['Last']))
        hour4[symbol['MarketName']].calculateChange(float(symbol['Last']))
        day1[symbol['MarketName']].calculateChange(float(symbol['Last']))


def getTime():
    return int(round(time.time() * 1000))

__main__()
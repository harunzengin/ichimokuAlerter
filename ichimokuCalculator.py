import numpy as np
from datetime import datetime
import json
from app import DiscordMessager
from app import screenShotGenerator
class ichmimokuCalculator:


    def __init__(self, symbol, api, params,interval):
        self.symbol = symbol
        self.api = api
        self.params = params
        self.interval = interval
        self.dataArray = np.array([0])
        self.ichimokuStatus = False
        self.current_high = 0.0
        self.current_low = 0.0

    def get_neccesaries(self, datalist):
        returndata = []
        if(self.api == "binance"):
            for window in datalist:
                returndata.append(list(map(float, window[2:4])))
            return np.array(returndata)
        else:
            return np.array(datalist)

    def get_symbol(self):
        return self.symbol

    def setInitialData (self, data):
        #global dataArray, ichimokuStatus, current_low,current_high
        self.dataArray = self.get_neccesaries(data)
        self.ichimokuStatus = False
        self.tenkan_sen = (float(self.dataArray[:,0][-(self.params[0]):].max()) + float(self.dataArray[:,1][-(self.params[0]):].min()))/2
        self.kijun_sen = ((self.dataArray[:,0][-self.params[1]:].max()) + (self.dataArray[:,1][-self.params[1]:].min()))/2
        self.senkou_span_A = (self.tenkan_sen + self.kijun_sen) / 2
        self.senkou_span_B = ((self.dataArray[:,0][-self.params[2]:].max()) + (self.dataArray[:,1][-self.params[2]:].min()))/2
        if(self.senkou_span_A >= self.senkou_span_B):
            self.ichimokuStatus = True
        else:
            self.ichimokuStatus = False
        self.current_high = self.dataArray[:,0][-1]
        self.current_low = self.dataArray[:,1][-1]

    def get_data(self):
        return self.data

    def calculateChange(self,currentPrice):
        if (currentPrice > self.current_high):
            self.current_high = currentPrice
            self.calculate_ichimoku()
        if (currentPrice < self.current_low):
            self.current_low = currentPrice
            self.calculate_ichimoku()

    def calculate_ichimoku(self):
        self.currentDataArray = self.dataArray.copy()
        highs = np.append(self.currentDataArray[:, 0][:-1], self.current_high).copy()
        lows = np.append(self.currentDataArray[:, 1][:-1], self.current_low).copy()
        tenkan_sen = (float(highs[-self.params[0]:].max()) + float(lows[-self.params[0]:].min())) / 2
        kijun_sen = (float(highs[-self.params[1]:].max()) + float(lows[-self.params[1]:].min())) / 2
        senkou_span_A = float(tenkan_sen + kijun_sen) / 2
        senkou_span_B = (float(highs[-self.params[2]:].max()) + float(lows[-self.params[2]:].min())) / 2
        #print ("Symbol   " + self.symbol + "   A: " + str(senkou_span_A) + " B: " + str(senkou_span_B) )

        if(self.ichimokuStatus == True and (senkou_span_A < senkou_span_B) and len(self.dataArray) >= max(self.params)):
            print("alert " + self.symbol + " from true to false in interval " + self.interval  + " where A : "  + str(senkou_span_A) + " B : " + str(senkou_span_B) +"   Time   "+ str(datetime.now()))
            self.ichimokuStatus = False

        if(self.ichimokuStatus == False and (senkou_span_A >= senkou_span_B) and len(self.dataArray) >= max(self.params)):
            self.ichimokuStatus = True
            print("alert " + self.symbol + " from false to true in interval " + self.interval + " where Senkou Span A : "  + str(senkou_span_A) + "Senkou Span B : " + str(senkou_span_B) + "  Time   "+ str(datetime.now()))
            sym = self.symbol
            if(self.api == "bittrex"):
                index = self.symbol.find('-')
                sym = self.symbol[index + 1:] + self.symbol[:index]
            interv = ""
            if self.interval == 'h':
                interv = "1H"
            elif self.interval == 'q':
                interv = "4H"
            elif self.interval == 'D':
                interv = "D"
            ex = "BINANCE" if self.api == "binance" else "BITTREX"
            DiscordMessager.sendMessage("Alert in " + sym + " in exchanghe " + ex + " in interval " +interv+" The tradingview link = https://www.tradingview.com/chart/?symbol=" + ex +":"+sym +"\n Screenshot link and Ichimoku URL to be sent soon.")
            links = screenShotGenerator.get_trading_view_graph(interval=self.interval, currency=sym,exchange=ex)
            DiscordMessager.sendMessage("Screenshot: " + links[0] + "   TradingView with Ichimoku link: " + links[1])


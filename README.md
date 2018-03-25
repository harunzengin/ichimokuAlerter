# ichimokuAlerter
An alarm for binance and bittrex that sends a message to a discord channel with a screenshot from TradingView, whenever any exchange's ichimoku cloud turns from red into green in any of 1H, 4H, 1D settings. 

## Getting Started



### Prerequisites

You need Python3, Selenium, Numpy, and Asyncio to be able to run this. 

```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get -y install python3-pip
pip3 install selenium
pip3 install numpy
pip3 install asyncio
```

### Installing

Just run 

```
python3 binancemain.py #optional 4 integers for ichimoku settings, seperated with spaces, default is 20 60 120 30
python3 binancemain.py <int> <int> <int> <int>
```
for the binance alarm and 

```
python3 bittrexmain.py #optional 4 integers for ichimoku settings, seperated with spaces, default is 20 60 120 30
python3 bittrexmain.py <int> <int> <int> <int>
```
for the bittrex alarm.


from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
webDriver = Firefox()
webDriver.get("https://www.tradingview.com/#signin")

#Log in to tradingview
def login(exchange):
#need two seperate tradingview accounts, premium if available, in order to prevent crashes, these are the accounts I created
# you may use them if they work
    if exchange == "binance":
        tradingViewuserName = "ichimokubot"
    else:
        tradingViewuserName = "ichimokubot1"
    tradingViewPassword = "abc123456"
    inputusername = webDriver.find_element_by_name("username")
    inputusername.send_keys(tradingViewuserName)
    inputpassword = webDriver.find_element_by_name("password")
    inputpassword.send_keys(tradingViewPassword)
    inputpassword.submit()
    time.sleep(3)

def get_trading_view_graph(interval, currency, exchange):
    webDriver.get("https://www.tradingview.com/chart/?symbol=" + exchange +":"+currency)
    intervalSelector = webDriver.find_element_by_class_name("value-DWZXOdoK-")
    intervalSelector.click()
    intervals = webDriver.find_elements_by_class_name("item-2xPVYue0-")
    if interval == 'h':
        intervals[6].click()
    elif interval == 'q':
        intervals[9].click()
    elif interval == 'd':
        intervals[10].click()
    time.sleep(2)
    screenshotbutton = webDriver.find_element_by_class_name("getimage")
    screenshotbutton.click()
    time.sleep(3)
    imageLink = webDriver.find_element_by_class_name("textInput-3WRWEmm7-")
    return( imageLink.get_attribute("value"), webDriver.current_url )


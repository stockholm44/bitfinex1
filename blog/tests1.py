from zipline.api import order, symbol
import matplotlib.pyplot as plt
from datetime import date
from urllib.request import urlopen, Request
from datetime import date
from datetime import datetime
from datetime import timedelta
from coin_raw_data_cmc import *
import pandas as pd
from zipline.algorithm import TradingAlgorithm

# print("Zipline setup?")

# a,b,c,d,e,f,g = cmc_data()
# # a = raw_data_1day('btc')
# print(b)

dates, opens, closes, highs, lows = raw_data_1day('BTC')

# print(closes)
# print(dates[0])
dates_str = []
for i, date in enumerate(dates):
    dates_str_temp = datetime.fromtimestamp(date)
    dates_str.append(dates_str_temp)

# print(dates_str)
def initialize(context):
    pass
#
def handle_data(context, data):
    order(symbol('BTC'),1)

data = pd.Series(closes, index = dates_str)
print(data)

algo = TradingAlgorithm(initialize = initialize, handle_data = handle_data)

result = algo.run(data)

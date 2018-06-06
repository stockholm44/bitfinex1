import requests
import json
import base64
import hmac
import hashlib
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from pandas import Series, DataFrame
from coin_raw_data_cmc_v1 import *
import pytz

from datetime import date
from datetime import datetime
from datetime import timedelta
from time import mktime
from calendar import *
#
dates, opens, closes, highs, lows = raw_data_1day('BTC')

btc_dict = {}
# btc_dict['date'] = []
# btc_dict['open'] = []
# btc_dict['close'] = []
# btc_dict['high'] = []
# btc_dict['low'] = []

# for i, line in enumerate(dates):
#     btc_dict['date'].append(dates[i])
#     btc_dict['open'].append(opens[i])
#     btc_dict['close'].append(closes[i])
#     btc_dict['high'].append(highs[i])
#     btc_dict['low'].append(lows[i])

# btc_dict['date'] = pd.to_datetime(dates, unit ='s')
btc_dict['date'] = dates
btc_dict['open'] = opens
btc_dict['close'] = closes
btc_dict['high'] = highs
btc_dict['low'] = lows
print('btc_dict ******************************')
print(btc_dict)

df = pd.DataFrame(btc_dict,columns =['open', 'close', 'high', 'low'], index= btc_dict['date'])

con = sqlite3.connect("c:/djangocym/bitfinex/blog/db/coin.db")

df.to_sql('btc_1day', con)

# df_read = pd.read_sql("SELECT * FROM btc2", con, index_col = 'date')
# df_read.index = pd.to_datetime(df_read.index)
df_read = pd.read_sql("SELECT * FROM btc_1day", con, index_col = 'index')
df_read.index = pd.to_datetime(df_read.index, unit = 's')
df_read.index = df_read.index.tz_localize('UTC')

# print(df_read.index)

print("time.time()",time.time())
test_datetime = pd.to_datetime(1525618800, unit = 's')
now_datetime = pd.to_datetime(time.time(), unit = 's')
# now_datetime_utc = df_read.index.tz_localize('UTC')
print("test_datetime",test_datetime)
print("now_datetime",now_datetime)
year = now_datetime.year
month = now_datetime.month
day = now_datetime.day
print(year, month, day)
today_utc_datetime = pd.Timestamp(year,month,day)
today_utc_epoch = (today_utc_datetime-pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
now_utc_epoch = (now_datetime-pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
print("today_utc_datetime",today_utc_datetime)
print("today_utc_epoch",today_utc_epoch)
print("now_utc_epoch", now_utc_epoch)

# print(now_datetime_utc)
# print(df_read)
# 잠시 주석화
# print(df_read)
# last_timestamp = df_read.index[-1]
# print(last_timestamp)
# last_datetime = datetime.fromtimestamp(last_timestamp).strftime('%Y.%m.%d %H:%M')
# print(last_datetime)

# last_datetime_2 = pd.to_datetime([1349720105,last_timestamp],unit = 's')
# print(last_datetime_2)
#
#
# print(pd.to_datetime(time.time(), unit = 's'))
# 여기까지 잠시 주석화





# rng_pytz = pd.date_range('3/6/2012 00:00', periods=10, freq='D',tz='Europe/London')
# print(rng_pytz)
#
# print('df ******************************')
# print(df)
#
# print('df.head() ******************************')
# print(df.head())
#
# print('df.tail() ******************************')
# print(df.tail())
#
# print('df.index ******************************')
# print(df.index)
#
# print('df.values ******************************')
# print(df.values)
#
# print('df.describe() ******************************')
# print(df.describe())
#
# print('df.T ******************************')
# print(df.T)

# print('df.sort_values(by="date") ******************************')
# print(df.sort_values(by='open',ascending = False))

# print(' ******************************')
# print(df.loc[df.index[0],'open'])
#
# print(' ******************************')
# print(df)
#
# print(' ******************************')
# df.loc[:,'open'] = np.array([5] * len(df))
# df = df[df>9000]
# print(' ******************************')
# print(df)

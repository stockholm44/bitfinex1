import pandas as pd
import sqlite3
from pandas import Series, DataFrame
from coin_raw_data_cmc import *

# raw_data = {'col0':[1,2,3,4], 'col1':[10,20,30,40],'col2':[100, 200, 300, 400]}
# df = DataFrame(raw_data)

# print(df)
#
# con = sqlite3.connect("c:/djangocym/bitfinex/blog/db/coin.db")
#
# df = pd.read_sql("SELECT * FROM kakao", con, index_col = 'Date')
#
# print(df)

#
dates, opens, closes, highs, lows = raw_data_1day('BTC')
#
btc_dict = {}
#
# for i, line in enumerate(dates):
btc_dict['date'] = dates
btc_dict['open'] = opens
btc_dict['high'] = highs
btc_dict['low'] = lows

# print(btc_dict)
df = DataFrame(btc_dict)
#
print(df)
con = sqlite3.connect("c:/djangocym/bitfinex/blog/db/test.db")
df.to_sql('btc2', con)

df_read = pd.read_sql("SELECT * FROM btc2", con, index_col = 'date')
df_read.index = pd.to_datetime(df_read.index)
#
print('df_read ******************************')
print(df_read)

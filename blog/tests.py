
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import mktime

import pandas as pd
import sqlite3
from pandas import Series, DataFrame
con = sqlite3.connect("c:/djangocym/bitfinex/blog/db/test.db")
df_read = pd.read_sql("SELECT * FROM btc2", con, index_col = 'date')

print(df_read.index[-1])
last_date = df_read.index[-2]
# print(df_read.index[0])
# print(df_read)

last_date_str = datetime.fromtimestamp(last_date).strftime('%Y%m%d%H%M%S')
print(last_date_str)

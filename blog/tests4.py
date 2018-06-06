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
# from coin_raw_data_cmc import *
import pytz

from datetime import date
from datetime import datetime
from datetime import timedelta
from time import mktime
from calendar import *

year = int(datetime.fromtimestamp(time.time()).strftime('%Y'))
month = int(datetime.fromtimestamp(time.time()).strftime('%m'))
day = int(datetime.fromtimestamp(time.time()).strftime('%d'))
hour = int(datetime.fromtimestamp(time.time()).strftime('%H'))

print(hour)
pd_t = pd.Timestamp('20180606')
print(pd_t)
minute = int(datetime.fromtimestamp(time.time()).strftime('%M'))
second = int(datetime.fromtimestamp(time.time()).strftime('%S'))

# print(year, month, day)
# print(type(year),type(month),type(day))

# url 불러올때 기간설정을 위한 str구현
now = datetime(year, month, day, hour, minute, second )
print(now)

rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
ts = pd.Series(np.random.randn(len(rng)), rng)
print(ts)
ts_utc = ts.tz_localize('UTC')

print(ts_utc)
# nowDate = now.strftime('%Y%m%d')
# past = now - timedelta(days = 30)
# pastDate = past.strftime('%Y%m%d')
# period_str = 'start=' + pastDate + '&end=' + nowDate

# 버전설명: 최초버전이후로 v1을 작성한다. 현재는 instant식으로 data를 크롤링 + API ticker를 이용해서 계속 raw_data만 갖고 했는데
#          이제 sqlite로 ohclv를 저장하여 trade data전체를 갖고 for문을 돌리는 시간을 아끼고자한다.
#          일단 이 파일자체는 coinmarketcap의 각 1일봉들을 가져올건데 database가 없으면 1달치를... 있다면 그 마지막날로부터 현재까지를 업데이트한다.
#          마지막날이 포함되는 이유는 database상 마지막날은 실시간현재 data가 반영. 그래서 불완전한 data임
#          그래서 마지막날 포함하여 현재날까지를 업데이트.
#          예상 막히는점.
#            1) dataframe을 정렬하기.
#            2) 마지막날의 ohclv data를 추가가 아닌 update형식으로 되는지 여부.
#            3) timestamp 다루기.날짜단위로 나와야하는데 애매한 단위가 되어 data를 왜곡시킬우려있음.


import requests
import json
import base64
import hmac
import hashlib
import time
from urllib.request import urlopen, Request
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import mktime
from calendar import *
from cmc import * # 현재날짜의 ohcl을 가져오기위함.

import pandas as pd
import sqlite3
from pandas import Series, DataFrame

# 크롤링을 위한 뷰티풀숲 소환.
from bs4 import BeautifulSoup
from urllib.request import urlopen

__all__ = ['cmc_data', 'raw_data_1day']



# 1. database에 저장된 1일봉중 맨마지막 날에 대한 timestamp 등 data 가져오기위함.
con = sqlite3.connect("c:/djangocym/bitfinex/blog/db/coin.db")
# coin.db에 btc_1day database가 btc 1일봉 data를 저장해놓은 databased임.
# 기존버전의 dates에 utc 기준으로 딱 떨어지는 시간이 아닌 15:00로 되있음-> 한국시간기준으로 utc가 -9니까 그걸로 설정된듯.
# 그래서 pd.to_datetime으로 utc기준으로 나오게 하고 그것을 epoch unixtime으로 저장하려함.
df_read = pd.read_sql("SELECT * FROM btc_1day", con, index_col = 'index')
df_read.index = pd.to_datetime(df_read.index, unit = 's')
df_read.index = df_read.index.tz_localize('UTC')

# database의 마지막 날짜 확인.
last_timestamp = df_read.index[-1]
print("last_timestamp",last_timestamp)

# 마지막날짜의 datetime 확인.
last_datetime = pd.to_datetime(last_timestamp,unit = 's')
print("last_datetime",last_datetime)

# 2. 현재날짜의 timestamp와 datetime 계산. 날짜단위 index를 위함.
#  2-1. 현재 시각의 timestamp와 datetime 계산. to_datetime의 unit = 's'는 epoch time 계산시 ns로 단위가 Default로 되어있어 꼭해줘야함.
now_datetime = pd.to_datetime(time.time(), unit = 's')
year = now_datetime.year
month = now_datetime.month
day = now_datetime.day

#  2-2. 날짜단위로 오늘날짜의 timestamp와 datetime 계산.
today_utc_datetime = pd.Timestamp(year,month,day)
today_utc_epoch = (today_utc_datetime-pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
print("today_utc_datetime",today_utc_datetime)
print("today_utc_epoch",today_utc_epoch)





# url 불러올때 기간설정을 위한 str구현
now = pd.to_datetime(today_utc_datetime, format = '%Y%m%d')
# print("now",now)
nowDate = now.strftime('%Y%m%d')
# print('nowDate',nowDate)
past = now - pd.Timedelta('30 days')
# print("past",past)
pastDate = past.strftime('%Y%m%d')
# print('pastDate',pastDate)
period_str = 'start=' + pastDate + '&end=' + nowDate
print(period_str)
# date_div = datetime(year, month, day, hour)
# date_div_ts = int(mktime(date_div.timetuple()))

# URL1 = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?"
URL1 = "https://coinmarketcap.com/currencies/"
URL3 = "/historical-data/?"

# # https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180413&end=20180513
# print('URL_cmc', URL_cmc)
# print('period_str', period_str)

def cmc_data():
    html = urlopen('https://coinmarketcap.com/')
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser")

    symbol = []
    symbol_name = []
    symbol_site = []
    symbol_market_cap = []
    symbol_circulating_supply = []
    symbol_percent_change = []
    symbol_price_usd = []
    symbol_volume_usd = []
    tbody_div = soup.find("tbody")
    tr_div = tbody_div.find_all("tr")

    #1
    for i, tr in enumerate(tr_div):
        td_name_div = tr.find("td",{"class":"no-wrap currency-name"})
        span_div = td_name_div.find("span",{"class":"currency-symbol"})
        symbol.append(span_div.text)

        a_div = span_div.find("a")
        href = a_div['href']
        href_split = href.split('/')
        symbol_site.append(href_split[2])

        symbol_name_temp = td_name_div.find("a",{'class':'currency-name-container'})
        symbol_name.append(symbol_name_temp.text)

        td_price_volume_div = tr.find_all("td",{"class":"no-wrap text-right"})
        # print('**********************************')
        # print('td_price_volume_div[0]',td_price_volume_div[0])
        a_price_div = td_price_volume_div[0].find("a",{'class':'price'})
        price = a_price_div['data-usd']
        symbol_price_usd.append(float(price))

        a_volume_div = td_price_volume_div[1].find("a",{'class':'volume'})
        # print('td_price_volume_div[1]',td_price_volume_div[1])
        volume = a_volume_div['data-usd']
        symbol_volume_usd.append(float(volume))
        # for i, td in enumerate(td_price_volume_div):
        #     print('**********************************')
        #     print('td',td)
        #     a_div = td.find("a",{'class':'price'})
        #     print('a_div',a_div)
        #     a_div_price = a_div['data-usd']
        #     print(a_div_price)
            # if a_div["class"] == 'price':   #여기가 틀렸는데.... 뭐가 틀린거지?
            #     symbol_price_usd_temp = a_div['data-usd']
            #     print('symbol_price_usd_temp',symbol_price_usd_temp)
            #     symbol_price_usd.append(symbol_price_usd_temp)
            # elif a_div['class'] == 'volume':
            #     symbol_volume_usd_temp = a_div['data-usd']
            #     print('symbol_volume_usd_temp',symbol_volume_usd_temp)
            #     symbol_volume_usd.append(symbol_volume_usd_temp)

        # td_percent_change_div = tr.find("td",{'class':"no-wrap percent-change  text-right negative_change"})
        # symbol_percent_change_temp = td_percent_change_div['data-percentusd']
        # symbol_percent_change.append(symbol_percent_change_temp)

        td_market_cap_div = tr.find("td",{'class':"no-wrap market-cap text-right"})
        symbol_market_cap_temp = td_market_cap_div['data-usd']
        symbol_market_cap.append(float(symbol_market_cap_temp))

        td_circulating_supply_div = tr.find("td",{'class':"no-wrap text-right circulating-supply"})
        symbol_circulating_supply_temp = td_circulating_supply_div['data-sort']
        symbol_circulating_supply.append(float(symbol_circulating_supply_temp))



    # for i, line in enumerate(symbol):
    #     print(i+1, symbol_name[i], symbol[i], symbol_site[i])

    #2
    # for i, tr in enumerate(tr_div):

    #
    #
    #
    # for i, line in enumerate(symbol):
    #     print(i+1, symbol_name[i], symbol[i], symbol_site[i], symbol_market_cap[i], symbol_circulating_supply[i], symbol_price_usd[i], symbol_volume_usd[i])
    # print(i+1, type(symbol_name[i]), type(symbol[i]), type(symbol_site[i]), type(symbol_market_cap[i]), type(symbol_circulating_supply[i]), type(symbol_price_usd[i]), type(symbol_volume_usd[i]))

    return symbol_name[:10], symbol[:10], symbol_site[:10], symbol_market_cap[:10], symbol_circulating_supply[:10], symbol_price_usd[:10], symbol_volume_usd[:10]

# 여기부터 뷰티풀 숲을 이용한 웹페이지 크롤링(코인마켓캡 coin별 1일봉 30일데이타.)
def raw_data_1day(coin):
    # 불러오기 위한 coin list를 cmc_data에서 불러오자.
    # 구지 아래와 같이 전부를 불러올 필요는 없지만 따로 함수를 구축해야하는건가 아니면 일부 list 만 뽑아올 수 있는게 있으면 나중에 수정.
    # 아래들중 원래는 symbol_site만 필요했지만 부가로 나머지들을 구축함self.
    symbol_name, symbol, symbol_site, symbol_market_cap, symbol_circulating_supply, symbol_price_usd, symbol_volume_usd = cmc_data()

    # 임시로 하는거 parameter인 coin에 해당하는 site symbol 찾기.(array쓰면 쉬웠을 것을 list로 일단 구현.)
    for i, symbol_site_temp in enumerate(symbol_site):
        if symbol[i] == coin:
            URL2 = symbol_site_temp
            break

    html = urlopen(URL1 + URL2 + URL3 + period_str)
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser")

    table_div = soup.find("table",{"class": "table"})
    tr_div = soup.find_all("tr",{"class": "text-right"})

    dates_str=[]
    dates=[]
    opens=[]
    closes=[]
    highs=[]
    lows=[]
    volumes=[]

    # 나중에는 아래와 같은 태그들을 이용해서 각 테이블의 열이 어떤건지도 검사하려고함.
    # 지금은 빠르게 코딩하는게 나으니까 아래것들은 나중에 추가하자.
    # <th class="text-left">Date</th>
    # <th class="text-right">Open</th>
    # <th class="text-right">High</th>
    # <th class="text-right">Low</th>
    # <th class="text-right">Close</th>
    # <th class="text-right">Volume</th>
    # <th class="text-right">Market Cap</th>

    # calendar를 이용해서 Jan, Feb등을 1, 2의 int로 표현하기 위해 dict를 만듬.
    # month_addr라는 "", Jan, Feb --- 등의 dict이 키와 value를 거꾸로 해서 만듬.
    # month_name은 January 등으로 풀네임임.(나중에 사용시 참고)
    month_num = dict((v,k) for k,v in enumerate(month_abbr))
    # print(month_num)

    for i, tr in enumerate(tr_div):
        # print('*************************')
        # print('i',i, tr)
        td_div = tr_div[i].find_all("td")
        for j, td in enumerate(td_div):
            # print('j',j, td)
            if j == 0:
                dates_str.insert(0, td.text)
            elif j == 1:
                opens.insert(0, float(td.text))
            elif j == 2:
                highs.insert(0, float(td.text))
            elif j == 3:
                lows.insert(0, float(td.text))
            elif j == 4:
                closes.insert(0, float(td.text))
            elif j == 5:
                volumes.insert(0, float(td.text.replace(",","")))

    # for i, line in enumerate(dates_str):
    #     print(dates_str[i], opens[i], closes[i], highs[i], lows[i], volumes[i])
        # print(type(dates[i]), type(opens[i]), type(closes[i]), type(highs[i]), type(lows[i]), type(volumes[i]))

    # float_string = "1,25"
    # a = float(str(float_string).replace(",", ""))
    # print(a)

    # date_srt에 저장한 May 09, 2018로 되어있는 str을 각각 년월일로 나누고 그것을 unixtime으로 바꾸어 dates(coin_index의 형식과 동일한)로 리스트화.
    for i, line in enumerate(dates_str):
        date_split = dates_str[i].split(' ')
        date_month = int(month_num[date_split[0]])
        date_day = int(date_split[1].split(',')[0])
        date_year = int(date_split[2])

        date_str = datetime(date_year, date_month, date_day)
        date_unix = int(mktime(date_str.timetuple()))

        date_str = pd.Timestamp(date_year, date_month, date_day)
        date_unix = (date_str-pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

        dates.append(date_unix)
    # for i, line in enumerate(dates):
        # print(dates_str[i], dates[i], closes[i])

    # 마지막 현재 시간의 bitcoin 가격을 넣기. 귀찮아서 OCHL은 다 마지막 가격으로설정.
    coin_data = ticker2('BTC')[0]
    price_usd = float(coin_data['price_usd']) # float
    date_unix = int(coin_data['last_updated'])
    dates.append(date_unix)
    opens.append(price_usd)
    closes.append(price_usd)
    highs.append(price_usd)
    lows.append(price_usd)

    return dates, opens, closes, highs, lows

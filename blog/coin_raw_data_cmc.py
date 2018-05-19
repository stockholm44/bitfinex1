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

# 크롤링을 위한 뷰티풀숲 소환.
from bs4 import BeautifulSoup
from urllib.request import urlopen

__all__ = ['raw_data_1day']

# 오로지 url불러올때 현재날짜와 1달전날짜를 소환하기위한 변수들임.
# (시간뒤부분빼려고 한거이므로 나중에 시간이후를 빼는 식이있으면 그걸로 대체가능)
# 아마 time.time()으로 초까지 설정하고 분/초 이후 단만 불러내서 그걸 빼는걸로 가능하지 않을까 생각해봄.
year = int(datetime.fromtimestamp(time.time()).strftime('%Y'))
month = int(datetime.fromtimestamp(time.time()).strftime('%m'))
day = int(datetime.fromtimestamp(time.time()).strftime('%d'))
# hour = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%H'))
# minute = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%M'))
# second = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%S'))

# print(year, month, day)
# print(type(year),type(month),type(day))

# url 불러올때 기간설정을 위한 str구현
now = datetime(year, month, day)
nowDate = now.strftime('%Y%m%d')
past = now - timedelta(days = 30)
pastDate = past.strftime('%Y%m%d')
period_str = 'start=' + pastDate + '&end=' + nowDate
# print(period_str)
# date_div = datetime(year, month, day, hour)
# date_div_ts = int(mktime(date_div.timetuple()))

URL_cmc = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?"
# # https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180413&end=20180513
# print('URL_cmc', URL_cmc)
# print('period_str', period_str)

def cmc_coin_list():
    html = urlopen('https://coinmarketcap.com/')
    source = html.read()
    html.close()
    soup = BeautifulSoup(source, "html.parser")

    symbol = []
    symbol_site = []
    tbody_div = soup.find("tbody")
    tr_div = tbody_div.find_all("tr")
    for i, tr in enumerate(tr_div):
        span_div = tr.find("span",{"class":"currency-symbol"})
    # span_div = tr_div.find("span",{"class":"currency-symbol"})
        symbol.append(span_div.text)
        a_div = span_div.find("a")
        href = a_div['href']
        href_split = href.split('/')
        symbol_site.append(href_split[2])
    for i, tr in enumerate(tr_div):
        td_div = td.find_all("td")
        td_a_div = td_div.find("a")
        print(td_a_div)

    return


# 여기부터 뷰티풀 숲을 이용한 웹페이지 크롤링(코인마켓캡 BTC 1일봉 30일데이타.)
def raw_data_1day():
    html = urlopen(URL_cmc + period_str)
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
        dates.append(date_unix)
    # for i, line in enumerate(dates):
        # print(dates_str[i], dates[i], closes[i])
    return dates, opens, closes, highs, lows


# a = month_abbr
# for i, line in enumerate(a):
#     print(a[i])
# b = month_name
# for i, line in enumerate(b):
#     print(b[i])
# month_num = dict((v,k) for k,v in enumerate(month_abbr))
# print(month_num)
# d = dict()
# print(type(d))
# e = {}
# print(type(e))

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
    print('**********************************')
    print('td_price_volume_div[0]',td_price_volume_div[0])
    a_price_div = td_price_volume_div[0].find("a",{'class':'price'})
    price = a_price_div['data-usd']
    print('price',price)
    print('td_price_volume_div[1]',td_price_volume_div[1])
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
    symbol_market_cap.append(symbol_market_cap_temp)

    td_circulating_supply_div = tr.find("td",{'class':"no-wrap text-right circulating-supply"})
    symbol_circulating_supply_temp = td_circulating_supply_div['data-sort']
    symbol_circulating_supply.append(symbol_circulating_supply_temp)



# for i, line in enumerate(symbol):
#     print(i+1, symbol_name[i], symbol[i], symbol_site[i])

#2
# for i, tr in enumerate(tr_div):

#
#
#
# for i, line in enumerate(symbol):
    # print(i+1, symbol_name[i], symbol[i], symbol_market_cap[i], symbol_circulating_supply[i], symbol_price_usd[i], symbol_volume_usd[i])
# , symbol_percent_change[i]
# print(symbol_name)
# print(symbol)
# print(symbol_market_cap)
# print(symbol_circulating_supply)
# print(symbol_price_usd)
# print(symbol_volume_usd)

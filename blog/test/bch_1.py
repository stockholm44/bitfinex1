import requests
import json
import base64
import hmac
import hashlib
import time
from datetime import date
from urllib.request import urlopen, Request
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import mktime


# Bitcoinchart로부터 URL 받기(시간제한을 URL + a 로 붙게 지정)
URL = "http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD"


# 각 시간간격을 Unixtime으로 표현
time_delta_15min = 60*15
time_delta_1hr = 60*60
time_delta_2hr = 60*60*2
time_delta_4hr = 60*60*2
time_delta_1day = 60*60*24
time_delta_30days = 60*60*24*30
time_delta_100days = 60*60*24*100


response = requests.get(URL)
splitResponse = response.text.splitlines()
splitResponse = splitResponse[::30]

splitline = []
timestamps = []
prices = []
amounts = []


# timestamp, price, amount 리스트에저장(날짜 내림차순으로)
for i, line in enumerate(splitResponse):
    splitline = splitResponse[i].split(',')
    timestamp = int(splitline[0])
    price = float(splitline[1])
    amount = float(splitline[2])

    timestamps.append(timestamp)
    prices.append(price)
    amounts.append(amount)



for i, line in enumerate(timestamps):
    print(i, timestamps[i])

# open, close, high, low +(날짜) 설정을 위한 리스트 작성.

year = int(datetime.fromtimestamp(timestamps[0]).strftime('%Y'))
month = int(datetime.fromtimestamp(timestamps[0]).strftime('%m'))
day = int(datetime.fromtimestamp(timestamps[0]).strftime('%d'))
hour = int(datetime.fromtimestamp(timestamps[0]).strftime('%H'))
minute = int(datetime.fromtimestamp(timestamps[0]).strftime('%M'))
second = int(datetime.fromtimestamp(timestamps[0]).strftime('%S'))

date_div = datetime(year, month, day, hour)
date_div_ts = int(mktime(date_div.timetuple()))


dates = []
opens = []
closes = []
highs = []
lows = []

open = close = high = low = prices[0]
dates.append(date_div_ts)
j = 0



# timestamp[0]의 시간중 시간까지만 끌어오기위해 임시로 사용.
# 나중에는 아래것을 따로 함수로 하나 만들어서 처리하자.

print("****Collecting open, close, high low ****************************")
for i in range(len(timestamps)):
    if timestamps[i] < date_div_ts:  # timestamp기준 하루이전이라면?
        j += 1
        date_div_ts -= time_delta_15min  # 기준일을 하루 낮추기
        open = prices[i-1]
        dates.insert(0, date_div_ts)       # 기준일을 date list에 추가
        opens.insert(0, open)
        closes.insert(0, close)
        highs.insert(0, high)
        lows.insert(0, low)
        close = high = low = prices[i]               # 하루전되기 마지막 거래가격을 close로 등록(?)

    if prices[i] > high:
        high = prices[i]

    if prices[i] < low:
        low = prices[i]

del dates[1]


for i in range(len(dates)):
    print(i, dates[i], opens[i], closes[i], highs[i], lows[i])


# RSI 계산을 위한
#1. AU, AD산출 후
#2. 14일간 rolling mean 구하기
#3. 14일째 후부터 RSI 산출

#1. AU, AD 산출
print("****Calculate dUp, dDown ****************************")
rsi = []
dUp = []
dDown = []
for i in range(len(dates)):
    if i > 0:
        if closes[i] >= closes[i-1]:
            dUp.append(closes[i]-closes[i-1])
            dDown.append(0)
            # print(i, ' dUp, dDown ',dUp[i], dDown[i])
        elif closes[i] < closes[i-1]:
            dUp.append(0)
            dDown.append(closes[i-1]-closes[i])
            # print(i, ' dUp, dDown ',dUp[i], dDown[i])
    elif i == 0:
        dUp.append(0)
        dDown.append(0)
        # print(i, ' dUp, dDown ',dUp[i], dDown[i])

for i in range(len(dates)):
    print(i, ' dUp, dDown ',dUp[i], dDown[i])
au = []
ad = []
rs = []
print("****Calculate au, ad, rs ****************************")
for i in range(len(dates)):
    if i < 14:
        au.append(0)
        ad.append(0)
        rs.append(0)
        rsi.append(50)
        print(i, 'i < 14', au[i], ad[i], rs[i],rsi[i])
    elif i == 14:
        dUp_Sum = dUp[1:15]
        # print('dUp_Sum', dUp_Sum)
        dDown_Sum = dDown[1:15]
        # print('dDown_Sum', dDown_Sum)
        au.append(sum(dUp_Sum)/len(dUp_Sum))
        ad.append(sum(dDown_Sum)/len(dDown_Sum))
        # print(i, 'au[i], ad[i]', au[i], ad[i])
        rs.append(au[i]/ad[i])
        rsi.append(100.0 - (100.0 / (1.0 + rs[i])))

    elif i > 14:
        au.append((au[i-1]*13+dUp[i])/14)
        ad.append((ad[i-1]*13+dDown[i])/14)
        rs.append(au[i]/ad[i])
        rsi.append(100.0 - (100.0 / (1.0 + rs[i])))

for i, line in enumerate(dates):
    print(i, dates[i], au[i], ad[i], rs[i], rsi[i])


# 각인덱스별로 읽어서 현재의 날짜기준으로 timestmap가 큰지 작은지 작으면 그 보다 아래 index를 만들어서 그다음엔 그날짜랑 비교하는 for문을 만들어야함.
# 그래서 일단 제일 마지막 행이 제일위로 오게 index sorting해야하고.
# 그리고 index 값 비교가능하게 if문 구성 -> if 기준날짜면 해당 시세를 open/close/high/low에 맞게 들어가게 다시 검사
#                                      -> if 기준날짜 아래면 기준날짜 - 1day에 해당하는 60*60*24f를 뺸 timestamp로

# df = pd.DataFrame({'Price' : float(splitline[1]), 'Amount' : float(splitline[2])}, index = [0]}, index = float(splitline[0]))
# print(df)

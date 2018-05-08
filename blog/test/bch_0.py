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

# Dataframe을 위한 모듈들
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Bitcoinchart로부터 URL 받기(시간제한을 URL + a 로 붙게 지정)
URL = "http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD"
# URL = "http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD"
# 거래 Raw data를 pandas의 dataframe으로 저장(open,close,high,low vs timestamp로 저장.)



# timestamp(unixtime)을 일반적인 날짜/시간표현으로 전환하기.
# 이걸 이용해서 해당 최후의 timestamp에서 기준 time을 정하고 거기서 계속 과거로 추산하자.
# timestamp = datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')
# timestamp_year = int(datetime.fromtimestamp(int("1284101485")).strftime('%Y'))
# timestamp_month = int(datetime.fromtimestamp(int("1284101485")).strftime('%m'))
# timestamp_day = int(datetime.fromtimestamp(int("1284101485")).strftime('%d'))
# timestamp_hour = int(datetime.fromtimestamp(int("1284101485")).strftime('%H'))
# timestamp_minute = int(datetime.fromtimestamp(int("1284101485")).strftime('%M'))
# timestamp_second = int(datetime.fromtimestamp(int("1284101485")).strftime('%S'))

# ref_date = datetime(timestamp_year, timestamp_month, timestamp_day)
# ref_date_unix = mktime(ref_date.timetuple())

# 현재 날짜/시간을 integer로 표현
year = int(datetime.now().strftime('%Y'))
month = int(datetime.now().strftime('%m'))
day = int(datetime.now().strftime('%d'))
hour = int(datetime.now().strftime('%H'))
minute = int(datetime.now().strftime('%M'))
second = int(datetime.now().strftime('%S'))

# 각 시간간격을 Unixtime으로 표현
time_delta_15min = 60*15
time_delta_1hr = 60*60
time_delta_2hr = 60*60*2
time_delta_4hr = 60*60*2
time_delta_1day = 60*60*24
time_delta_30days = 60*60*24*30
time_delta_100days = 60*60*24*100

# 오늘 날짜를 unixtime으로 참고
date_div = datetime(year, month, day, hour)
date_div_ts = int(mktime(date_div.timetuple()))
print("date div: ", date_div)
print("date div to timestamp: ", date_div_ts)
print("type : ", type(date_div_ts))

# adjustedTime = 0
# adjustedTime = date_div_ts - time_delta_1day
# adjustedTime = date_div_ts - time_delta_1day*5
# adjustedTime = int(time.time())
# print("time.time()",time.time())
# print(datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
# response = requests.get(URL+"&start="+str(adjustedTime))
# response = requests.get(URL + str(adjustedTime))
response = requests.get(URL)
splitResponse = response.text.splitlines()
splitResponse = splitResponse[::30]
# print(splitResponse)
# print(type(splitResponse))
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
    # print(timestamps)
# print("timestamps : ", timestamps)
# print("prices : ", prices)
# print("amounts : ", amounts)

# print(date_div)
# print(date_div_ts)
# for i in range(len(splitResponse)):
#     print(timestamps[i], datetime.fromtimestamp(int(timestamps[i])).strftime('%Y-%m-%d %H:%M:%S'), prices[i], amounts[i])
# print("Length of timestamps: ",len(timestamps))
# df = pd.DataFrame({"prices":prices,"amounts":amounts}, index = timestamps)

# open, close, high, low +(날짜) 설정을 위한 리스트 작성.
dates = []
opens = []
closes = []
highs = []
lows = []
# for i in range(len(timestamps)):
#     print("timestamps : ", timestamps[i], "prices : ", prices[i])
open = close = high = low = prices[0]
dates.append(date_div_ts)
j = 0
# print(len(timestamps))
# for i in range(len(prices)):
# print("timestamps[0]",timestamps[0])
# print("date_div_ts",date_div_ts)

# 각 리스트에 open,close,high,low 저장(날짜 오름차순으로 )
# -> 오름차순으로의 이유는 RSI 계산시 첫 14일에 대해서는 계산안하고 15일쨰 처음 SMA로 계산하고 그다음은 EMA로 계산할거기때문.

#date_div_ts 다시 설정해보자. timestamps[0]의 시간까지만 읽고 분, 초는 버리고 그걸 다시 Unixtime으로



# timestamp[0]의 시간중 시간까지만 끌어오기위해 임시로 사용.
# 나중에는 아래것을 따로 함수로 하나 만들어서 처리하자.
year = int(datetime.fromtimestamp(timestamps[0]).strftime('%Y'))
month = int(datetime.fromtimestamp(timestamps[0]).strftime('%m'))
day = int(datetime.fromtimestamp(timestamps[0]).strftime('%d'))
hour = int(datetime.fromtimestamp(timestamps[0]).strftime('%H'))
minute = int(datetime.fromtimestamp(timestamps[0]).strftime('%M'))
second = int(datetime.fromtimestamp(timestamps[0]).strftime('%S'))

date_div = datetime(year, month, day, hour)
date_div_ts = int(mktime(date_div.timetuple()))

# print("int(timestamp[0])", int(timestamps[0]), "date_div_ts", date_div_ts)

print("****Collecting open, close, high low ****************************")
for i in range(len(timestamps)):
    # print(i, datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d %H:%M:%S'),int(timestamps[i]), "date_div_ts", date_div_ts)

    if timestamps[i] < date_div_ts:  # timestamp기준 하루이전이라면?
        # print('Next Date Time')
        j += 1
        date_div_ts -= time_delta_1hr  # 기준일을 하루 낮추기
        # print(date_div_ts)
        open = prices[i-1]
        dates.insert(0, date_div_ts)       # 기준일을 date list에 추가
        opens.insert(0, open)
        closes.insert(0, close)
        highs.insert(0, high)
        lows.insert(0, low)
        # print('------------------------------------',dates[1], opens[0], closes[0], highs[0], lows[0])
        close = high = low = prices[i]               # 하루전되기 마지막 거래가격을 close로 등록(?)
        # print(dates[j-1], opens[j-1], closes[j-1], highs[j-1], lows[j-1])
    # print("prices[i] > high??",prices[i] ,high)
    if prices[i] > high:
        high = prices[i]
        # print("Yes, high = prices[i] ->",high)
    # print("prices[i] < low??",prices[i] ,low)
    if prices[i] < low:
        low = prices[i]
        # print("Yes, low = prices[i] ->",low)


del dates[1]
# print("dates length", len(dates))
# print("len(dates)?", len(dates))
# print("len(opens)?", len(opens))
# print("len(closes)?", len(closes))
# print("len(highs)?", len(highs))
# print("len(lows)?", len(lows))


for i in range(len(dates)):
    print(i, dates[i], opens[i], closes[i], highs[i], lows[i])
# print("timestamps[0],timestamps[-1]", timestamps[0],timestamps[-1])
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

        # for i in enumerate(dUp_Sum):
        #     print(i, 'dUp_Sum, dDown_Sum', dUp_Sum[i], dDown_Sum[i])
        # dUp_Sum = 0
        # dDown_Sum = 0
        # for j in range(14):
        #     print('i, j, i-j', i, j, i-j)
        #     dUp_Sum += dUp[i-j]
        #     print('dUp_Sum += dUp[i-j]', dUp_Sum, dUp[i-j])
        #     dDown_Sum += dDown[i-j]
        #     print('dDown_Sum += dDown[i-j]', dDown_Sum, dDown[i-j])
        #
        #     au.append(dUp_Sum/14)
        #     ad.append(dDown_Sum/14)
        #     rs.append(au[i]/ad[i])
        #     print('dUp_Sum/14,dDown_Sum/14',dUp_Sum/14,dDown_Sum/14 )
        #     print('au[i], ad[i]',au[i], ad[i])
        #     # print('au : ',au)
        #     # print('ad ', ad)
        # print(i, 'i == 14', au[i], ad[i], rs[i], rsi[i])
    elif i > 14:
        au.append(((au[i-1]/13)+dUp[i])/14)
        ad.append(((ad[i-1]/13)+dDown[i])/14)
        rs.append(au[i]/ad[i])
        rsi.append(100.0 - (100.0 / (1.0 + rs[i])))
        # print(i, 'i > 14', au[i], ad[i], rs[i], rsi[i])
#
for i, line in enumerate(dates):
    print(i, au[i], ad[i], rs[i], rsi[i])
#
# print(dates)
print(len(dates))


# 각인덱스별로 읽어서 현재의 날짜기준으로 timestmap가 큰지 작은지 작으면 그 보다 아래 index를 만들어서 그다음엔 그날짜랑 비교하는 for문을 만들어야함.
# 그래서 일단 제일 마지막 행이 제일위로 오게 index sorting해야하고.
# 그리고 index 값 비교가능하게 if문 구성 -> if 기준날짜면 해당 시세를 open/close/high/low에 맞게 들어가게 다시 검사
#                                      -> if 기준날짜 아래면 기준날짜 - 1day에 해당하는 60*60*24f를 뺸 timestamp로

# df = pd.DataFrame({'Price' : float(splitline[1]), 'Amount' : float(splitline[2])}, index = [0]}, index = float(splitline[0]))
# print(df)

def trades(): # gets the innermost bid and asks and information on the most recent trade.
    adjustedTime = int(time.time()) - time_delta_30days
    response = requests.get(URL + str(adjustedTime))
    print(response)

    splitResponse = response.text.splitlines()
    prices = []
    timestamps = []
    amounts = []
    mymax = 0

    #Only keep one of each 30 lines
    splitResponse = splitResponse[::30]

    for i,line in enumerate(splitResponse):
        splitline = splitResponse[i].split(',')
        timestamp = splitline[0]
        price = round(float(splitline[1]),2)
        amount = round(float(splitline[2]),8)
        #print "amount: " + str(amount)
        if mymax < amount:
           mymax = amount
        timestamps.append(float(timestamp))
        prices.append(float(price))
        amounts.append(float(amount)*5 )
    #print "mymax: " + mymax
    #plt.scatter(timestamps, prices, s=amounts, alpha=.2)
    plt.plot(timestamps, prices, 'k-', linewidth=.7)
    plt.show()

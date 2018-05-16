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
from coin_raw_data_cmc import *

# Bitcoinchart로부터 URL 받기(시간제한을 URL + a 로 붙게 지정)
URL = "http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD&start="

# 위 URL 설명
# 위와 같이 그냥 symbol만 입력되있으면 response로 큰숫자부터 시작하는 내림차순으로 받아짐.
# &start= 을 붙이기만 한 것은 위의 결과와 동일
# 하지만 &start= + str(숫자)가 들어 가게 되면 해당 숫자부터 최근날짜 방향으로 20000개가 오름차순으로 받아짐.
# 즉 처음은 그냥 내림차순 그대로 받아서 아래의 RSI 받는 거 그대로 하면 되고
# 그 이후에 첫 timestamp의 끝에거 기준으로 20000개를 받게되니까 대략적인 예측으로 떄려맞춰야하나....
# 보통 20000개 timestamp에 몇시간정도인지 보자. 대충보니 16시간정도. 12시간 단위로 불러내면 10개정도면 충분.



# 각 시간간격을 Unixtime으로 표현
time_delta_15min = 60*15
time_delta_1hr = 60*60
time_delta_2hr = 60*60*2
time_delta_6hr = 60*60*6
time_delta_10hr = 60*60*10
time_delta_10hr = 60*60*12
time_delta_1day = 60*60*24


# response 받는곳 부터 for 문으로 5일치를 받아놓자.
# 5일치가 그냥 넘어가버릴수도 있으니까 0으로 했을때의 timestamp를 저장해서 그시점이 왔을떄 정지 시키든가.
# 20000개씩밖에 못받으니까 나눠서 5일치를 받아보자.


# 나중에는 해당데이터를 ohcl만 서버에 저장해서 구지 불러들일필요없게하자.
# 서버에서는 5일에 한번은 실행시켜 없는 timestamp에 대해서만 불러올수 있게 하자.
# 안그러면 실행속도가 너무 느리다.


# 날짜를 내림차순으로 정렬
# raw_data 끌어오는게 시간이 은근걸려서 num_times 를 매개변수로 시간을 절약해보자
# 15분봉 - 2 5초
# 1시간 - 3  11초
# 2시간 - 4  15초
# 6시간 - 9 - 47초
# 위의 결과로 효율성을 위해 4번까지만 돌려야할듯.
def raw_data():

    splitline = []

    timestamps_sum = []
    prices_sum = []
    amounts_sum = []

    for j in range(1,4):
        # print('for j in range(1,3):', j)
        adjustedTime = int(time.time()) - time_delta_10hr * j
        response = requests.get(URL + str(adjustedTime))
        splitResponse = response.text.splitlines()
        splitResponse = splitResponse[::30] # 30 step 단위만 저장.(너무 Data가 비슷/중복되게 많아서 step 넣음.)

        timestamps = []
        prices = []
        amounts = []

        # timestamp, price, amount 리스트에저장(날짜 내림차순으로)
        for i, line in enumerate(splitResponse):
            splitline = splitResponse[i].split(',')
            timestamp = int(splitline[0])
            price = float(splitline[1])
            amount = float(splitline[2])

            timestamps.insert(0, timestamp)
            prices.insert(0, price)
            amounts.insert(0, amount)
        if j == 1 :
            # timestamps_last = timestamps[-1]
            timestamps_last_list = timestamps[-31:-1]
            # print("timestamps_last_list",j, timestamps_last_list)


        # print(j, timestamps)
        # print(timestamps[-31:-1])
        if j > 1:
            timestamps_last_index = 0
            for i, line in enumerate(timestamps_last_list):
                try:
                    timestamps_last_index = timestamps.index(timestamps_last_list[i])
                    # for k, line in enumerate(timestamps_last_list):
                    #     print(k, timestamps_last_list(k))
                    # for k, line in enumerate(timestamps_last_list):
                    #     print(k, timestamps(k))
                    # print('timestamps',timestamps)

                except Exception:
                    pass
            # for k, line in enumerate(timestamps_last_list):
            #     print(k, timestamps_last_list[k])
            # for k, line in enumerate(timestamps):
            #     print(k, timestamps[k])
            # print('timestamps_last_index',j, timestamps_last_index)
            # timestamps_last_index = timestamps.index(timestamps_last)
            # print(j,'timestamps_last_index', timestamps_last_index)
            # print('timestamps_last_index', j , timestamps_last_index)
            timestamps = timestamps[timestamps_last_index:]
            # print(j,'timestamps[-1]',timestamps[-1])
            timestamps_last_list = timestamps[-31:-1]
        # for k, line in enumerate(timestamps):
        #     print(k, timestamps[k])
        timestamps_sum += timestamps
        prices_sum += prices
        amounts_sum += amounts
        # print("timestamps_sum",j, timestamps_sum)

    return timestamps_sum, prices_sum, amounts_sum





# open, close, high, low +(날짜) 설정을 위한 리스트 작성.
# 날짜를 오름차순으로 정렬
def ochl_data(period, timestamps_sum, prices_sum, amounts_sum):

    # timestamps_sum, prices_sum, amounts_sum = raw_data()
    time_delta= period  # 여러개의 period를 받아서 date_div_ts에서 시간간격을 뺴주는 time_delta를 정의함.

    year = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%Y'))
    month = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%m'))
    day = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%d'))
    hour = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%H'))
    minute = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%M'))
    second = int(datetime.fromtimestamp(timestamps_sum[0]).strftime('%S'))

    date_div = datetime(year, month, day, hour)
    date_div_ts = int(mktime(date_div.timetuple()))


    dates = []
    opens = []
    closes = []
    highs = []
    lows = []

    open = close = high = low = prices_sum[0]
    dates.append(date_div_ts)
    j = 0



    # timestamp[0]의 시간중 시간까지만 끌어오기위해 임시로 사용.
    # 나중에는 아래것을 따로 함수로 하나 만들어서 처리하자.

    # print("****Collecting open, close, high low ****************************")
    for i in range(len(timestamps_sum)):
        if timestamps_sum[i] < date_div_ts:  # timestamp기준 하루이전이라면?
            j += 1
            date_div_ts -= time_delta  # 기준일을 하루 낮추기
            open = prices_sum[i-1]
            dates.insert(0, date_div_ts)       # 기준일을 date list에 추가
            opens.insert(0, open)
            closes.insert(0, close)
            highs.insert(0, high)
            lows.insert(0, low)
            close = high = low = prices_sum[i]               # 하루전되기 마지막 거래가격을 close로 등록(?)

        if prices_sum[i] > high:
            high = prices_sum[i]

        if prices_sum[i] < low:
            low = prices_sum[i]

    del dates[1]

    return dates, opens, closes, highs, lows


# for i in range(len(dates)):
#     print(i, dates[i], opens[i], closes[i], highs[i], lows[i])



# RSI 계산을 위한 함수. 단 ochl_data와 동일하게 period 호출값을 받아서 retrun 시킴.
# 날짜를 오름차순으로 정렬
def rsi(period, a=False, b=False, c=False): # ★★★★★★180514 하려는건 rsi에 option으로 a, b, c 리스트를 넣으려고하는거, 왜냐면 1day면 아예 필요없고 그이외일때만 필요하므로.
    if period == time_delta_1day:
        dates, opens, closes, highs, lows = raw_data_1day()
        # print('raw_data_1day')
        # for i in range(len(dates)):
        #     print(i, dates[i], opens[i], closes[i], highs[i], lows[i])
    elif period in [time_delta_15min, time_delta_1hr, time_delta_2hr]:
        # print('ochl_data')
        dates, opens, closes, highs, lows = ochl_data(period, a, b, c)
    else:
        print("what the fuck")
    # RSI 계산을 위한
    #1. AU, AD산출 후
    #2. 14일간 rolling mean 구하기
    #3. 14일째 후부터 RSI 산출

    #1. AU, AD 산출
    # print("****Calculate dUp, dDown ****************************")
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

    # for i in range(len(dates)):
    #     print(i, ' dUp, dDown ',dUp[i], dDown[i])
    au = []
    ad = []
    rs = []
    # print("****Calculate au, ad, rs ****************************")
    for i in range(len(dates)):
        if i < 14:
            au.append(0)
            ad.append(0)
            rs.append(0)
            rsi.append(50)
            # print(i, 'i < 14', au[i], ad[i], rs[i],rsi[i])
        elif i == 14:
            dUp_Sum = dUp[1:15]
            # print('dUp_Sum', dUp_Sum)
            dDown_Sum = dDown[1:15]
            # print('dDown_Sum', dDown_Sum)
            au.append(sum(dUp_Sum)/len(dUp_Sum))
            ad.append(sum(dDown_Sum)/len(dDown_Sum))
            # print(i, 'au[i], ad[i]', au[i], ad[i])
            rs.append(au[i]/ad[i])
            rsi.append(format(100.0 - (100.0 / (1.0 + rs[i])),'.2f'))

        elif i > 14:
            au.append((au[i-1]*13+dUp[i])/14)
            ad.append((ad[i-1]*13+dDown[i])/14)
            rs.append(au[i]/ad[i])
            rsi.append(format(100.0 - (100.0 / (1.0 + rs[i])),'.2f'))
    #
    # for i, line in enumerate(dates):
    #     print(i, dates[i], closes[i], rsi[i])
    # print(len(dates))
    # print(len(closes))
    # print(len(rsi))

    return dates, closes, rsi

# def rsi_values():
#     timestamps_sum, prices_sum, amounts_sum = raw_data()
#     rsi_value_list = []
#     time_delta_list = [time_delta_15min, time_delta_1hr, time_delta_2hr, time_delta_1day]
#     for i, rsi in enumerate(time_delta_list):
#         if rsi == time_delta_1day:
#             dates, closes, rsi = rsi(rsi)
#         else:
#             dates, closes, rsi = rsi(rsi, timestamps_sum, prices_sum, amounts_sum)
#         rsi_value_list.append(rsi[-1])
#     for i, line in enumerate(time_delta_list):
#         print('time_delta = ', time_delta_list[i], 'rsi = ', rsi_value_list[i])
#
#     return time_delta_list, rsi_value_list
#
# a, b = rsi_values()


def rsi_values():
    timestamps_sum, prices_sum, amounts_sum = raw_data()
    rsi_value_list = []
    time_delta_list = [time_delta_15min, time_delta_1hr, time_delta_2hr, time_delta_1day]
    time_delta_list_name = ['15min', '1hr', '2hr', '1day']

    # print(time_delta_list)
    for i, time_delta in enumerate(time_delta_list):
        # print('time_delta',time_delta)
        if time_delta == time_delta_1day:
            dates, closes, rsi_list = rsi(time_delta)   # 여가서 원래 rsi_list를 rsi라고 해서 TypeError: 'list' object is not callable 에러떴었음. 아마 함수 rsi 와 이름이 동일해서 그런듯.

            # for i, line in enumerate(dates):
            #     print(i, dates[i], closes[i], rsi_list[i])
        else:
            dates, closes, rsi_list = rsi(time_delta, timestamps_sum, prices_sum, amounts_sum)
            # for i, line in enumerate(dates):
            #     print(i, dates[i], closes[i], rsi_list[i])
        rsi_value_list.append(rsi_list[-1])



    # for i, line in enumerate(time_delta_list):
    #     print('time_delta = ', time_delta_list, 'rsi = ', rsi_value_list)

    return time_delta_list, time_delta_list_name, rsi_value_list

# time_delta_list, time_delta_list_name, rsi_value_list = rsi_values()
# for i, line in enumerate(time_delta_list):
#     print(i, 'time_delta_list_name = ', time_delta_list_name[i], 'rsi = ', rsi_value_list[i])

#
# a, b, c = raw_data()
#
# dates2, closes2, rsi2 = rsi(time_delta_15min,a,b,c)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates2):
#     print(i, dates2[i], closes2[i], rsi2[i])
#
# dates3, closes3, rsi3 = rsi(time_delta_1hr,a,b,c)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates3):
#     print(i, dates3[i], closes3[i], rsi3[i])
#


# timestamps_sum, prices_sum, amounts_sum = raw_data()
#
# dates2, closes2, rsi2 = rsi(time_delta_15min,timestamps_sum, prices_sum, amounts_sum)
# print('time_delta_15min : ',time_delta_15min)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates2):
#     print(i, dates2[i], closes2[i], rsi2[i])
# dates3, closes3, rsi3 = rsi(time_delta_1hr,timestamps_sum, prices_sum, amounts_sum)
# print('time_delta_1hr : ',time_delta_1hr)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates3):
#     print(i, dates3[i], closes3[i], rsi3[i])
# dates4, closes4, rsi4 = rsi(time_delta_1day)
# print('time_delta_1day : ',time_delta_1day)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates4):
#     print(i, dates4[i], closes4[i], rsi4[i])



# timestamps_sum, prices_sum, amounts_sum = raw_data()
# print("Raw Data Function Result**********************")
# for i, line in enumerate(timestamps_sum):
#     print(i, timestamps_sum[i], prices_sum[i])
#
# dates1, opens1, closes1, highs1, lows1 = ochl_data(time_delta_1hr)
# print("OCHL Data Function Result**********************")
# for i, line in enumerate(dates1):
#     print(i, dates1[i], closes1[i])
#
#
# #
# a, b, c = raw_data()
# dates2, closes2, rsi2 = rsi(time_delta_15min,a,b,c)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates2):
#     print(i, dates2[i], closes2[i], rsi2[i])
# dates3, closes3, rsi3 = rsi(time_delta_1hr,a,b,c)
# print("RSI Function Result**********************")
# for i, line in enumerate(dates2):
#     print(i, dates2[i], closes2[i], rsi2[i])


# 각인덱스별로 읽어서 현재의 날짜기준으로 timestmap가 큰지 작은지 작으면 그 보다 아래 index를 만들어서 그다음엔 그날짜랑 비교하는 for문을 만들어야함.
# 그래서 일단 제일 마지막 행이 제일위로 오게 index sorting해야하고.
# 그리고 index 값 비교가능하게 if문 구성 -> if 기준날짜면 해당 시세를 open/close/high/low에 맞게 들어가게 다시 검사
#                                      -> if 기준날짜 아래면 기준날짜 - 1day에 해당하는 60*60*24f를 뺸 timestamp로

# df = pd.DataFrame({'Price' : float(splitline[1]), 'Amount' : float(splitline[2])}, index = [0]}, index = float(splitline[0]))
# print(df)

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
time_delta_1day = 60*60*24
time_delta_30days = 60*60*24*30
time_delta_100days = 60*60*24*100

# response 받는곳 부터 for 문으로 5일치를 받아놓자.
# 5일치가 그냥 넘어가버릴수도 있으니까 0으로 했을때의 timestamp를 저장해서 그시점이 왔을떄 정지 시키든가.
# 20000개씩밖에 못받으니까 나눠서 5일치를 받아보자.

splitline = []

timestamps_sum = []
prices_sum = []
amounts_sum = []

for j in range(1,5):
    adjustedTime = int(time.time()) - time_delta_10hr * j
    response = requests.get(URL + str(adjustedTime))
    splitResponse = response.text.splitlines()
    splitResponse = splitResponse[::10] # 30 step 단위만 저장.(너무 Data가 비슷/중복되게 많아서 step 넣음.)

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

    print(timestamps)

#     if j == 1 :
#         # timestamps_last = timestamps[-1]
#         timestamps_last_list = timestamps[-31:-1]
#         print("at j ==1 timestamps_last_list", timestamps_last_list)
#     # print(j, timestamps)
#     # print(timestamps[-31:-1])
#     if j > 1:
#         for i, line in enumerate(timestamps_last_list):
#             try:
#                 print("timestamps_last_list index matching before timestamps",timestamps)
#                 timestamps_last_index = timestamps.index(timestamps_last_list[i])
#             except Exception:
#                 pass
#         # timestamps_last_index = timestamps.index(timestamps_last)
#         # print(j,'timestamps_last_index', timestamps_last_index)
#         timestamps = timestamps[timestamps_last_index:]
#         # print(j,'timestamps[-1]',timestamps[-1])
#         timestamps_last_list = timestamps[-31:-1]
#     timestamps_sum += timestamps
#     prices_sum += prices
#     amounts_sum += amounts
#
#
# for i, line in enumerate(timestamps_sum):
#     print(i, timestamps_sum[i], prices_sum[i])

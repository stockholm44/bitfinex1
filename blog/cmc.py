# Coinmarketcap.com의 API Data 기반으로 Django로 쏴주기

import requests
import json
import base64
import hmac
import hashlib
import time
from urllib.request import urlopen, Request

def ticker(number):
	URL = "https://api.coinmarketcap.com/v1/ticker/?convert=KRW&limit=%d" % number
	response = requests.request("GET", URL)
	rep = response.json()
	# bid = rep['bid']
	return rep

a = ticker(10)
print(a)
print(a[0])
print(a[0]['name'])
b= "BTC"
for i in range(9):
    if a[i]['symbol'] == b:
        raw = i
price_usd = a[raw]['price_usd']
name = a[raw]['name']

print(price_usd)
print(type(price_usd))
price_usd = format(float(a[raw]['price_usd']),',.2f')
price_krw = format(float(a[raw]['price_krw']),',.0f')
print(name)
print(price_usd)
print(price_krw)

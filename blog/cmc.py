# Coinmarketcap.com의 API Data 기반으로 Django로 쏴주기

import requests
import json
import base64
import hmac
import hashlib
import time
from urllib.request import urlopen, Request

__all__ = ['ticker1','ticker2']

def ticker1(number):
	URL = "https://api.coinmarketcap.com/v1/ticker/?convert=KRW&limit=%d" % number
	response = requests.request("GET", URL)
	rep = response.json()
	# bid = rep['bid']
	return rep

def ticker2(data):
	coin_symbols = {'BTC':'Bitcoin', 'ETH':'Ethereum', 'XRP':'Ripple'}
	coin_keys = coin_symbols.keys()
	if data in coin_keys:
		symbol = coin_symbols[data]
	URL = "https://api.coinmarketcap.com/v1/ticker/%s/?convert=KRW" % symbol
	response = requests.request("GET", URL)
	rep = response.json()
	# bid = rep['bid']
	return rep
# 
# a = ticker2('BTC')
# print(a)
# print(a[0])

# coin_symbols = {'BTC':'Bitcoin', 'ETH':'Ethereum', 'XRP':'Ripple'}
# coin_keys = coin_symbols.keys()
#
# data = 'BTC'
# if data in coin_keys:
# 	symbol = coin_symbols[data]
# 	print(symbol)
#
# URL = "https://api.coinmarketcap.com/v1/ticker/%s/?convert=KRW" % coin_key
# response = requests.request("GET", URL)
# rep = response.json()
#
# a = ticker2('BTC')
# print(a)

# a = ticker(10)
# print(a)
# print(a[0])
# print(a[0]['name'])
# b= "BTC"
# for i in range(9):
#     if a[i]['symbol'] == b:
#         raw = i
# price_usd = a[raw]['price_usd']
# name = a[raw]['name']
#
# print(price_usd)
# print(type(price_usd))
# price_usd = format(float(a[raw]['price_usd']),',.2f')
# price_krw = format(float(a[raw]['price_krw']),',.0f')
# print(name)
# print(price_usd)
# print(price_krw)

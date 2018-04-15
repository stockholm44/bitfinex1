import requests
import json
import base64
import hmac
import hashlib
import time
from urllib.request import urlopen, Request
#
# url = "https://api.bitfinex.com/v1/pubticker/btcusd"
#
# response = requests.request("GET", url)
#
# print(response.text)


# __all__ = ['ticker', 'today', 'orderbook', 'lendbook', 'stats', 'trades', 'lends', 'symbols', 'place_order', 'delete_order', 'delete_all_order', 'status_order', 'active_orders', 'active_positions', 'place_offer', 'cancel_offer', 'status_offer', 'active_offers', 'past_trades', 'balances', 'claim_position', 'close_position', 'withdraw']
#
# URL = "https://api.bitfinex.com/v1"

# fp = open("../keys.txt")

# API_KEY = fp.readline().rstrip() # put your API public key here.
# API_SECRET = fp.readline().rstrip() # put your API private key here.
# print ("Your pub: " + str(API_KEY))
#print "Your priv: " + str(API_SECRET)

# unauthenticated

# Bitfinex API
def bid_Finex(symbol):
	URL = "https://api.bitfinex.com/v1/pubticker/%s" % symbol
	response = requests.request("GET", URL)
	rep = response.json()
	bid = rep['bid']
	return bid

# # coinone API
# def bid_Coinone():
# 	URL = "https://api.coinone.co.kr/ticker/"
# 	response = requests.request("GET", URL)
# 	rep = response.json()
# 	bid = rep['last']
# 	return bid
# 
# def gimp():
# 	finex = float(bid_Finex('btcusd'))
# 	coinone = int(bid_Coinone())
# 	gimp_btc = float(coinone/finex/1069-1)
# 	return str(format(gimp_btc*100, '.2f')+"%")
#
# print(gimp())
#
# a=bid_Coinone()
# print(a)

# Bitcoinchart API
#
# url = "https://data.fixer.io/api/latest"
#
# response = requests.request("GET", url)
# print(response.text)
# rep = response.json()
# # print(rep)
# rep1= len(rep)
# for i in range(rep1):
# 	print(rep[i])
#
# url = "https://api.coinone.co.kr/orderbook/eth/"
#
# response = requests.request("GET", url)
#
# print(response.text)
#
# data = get_response('v2/transaction/history/', create_payload({
#     'currency': 'btc',
# }))
# bb= bid('btcusd')
# print(bb)
# bb= bid('ethusd')
# print(bb)

# url = "https://api.bitfinex.com/v1/pubticker/ethusd"
#
# response = requests.request("GET", url)
#
# print(response.text)


# response_Dict = ast.literal_eval(self.response.text)
# print(response_Dict)
# def bid_Finex(self):
# 	self.bid_Finex_Data = self.response_Dict['bid']
# 	return self.bid_Finex_Data


# def ticker(symbol='btcusd'): # gets the innermost bid and asks and information on the most recent trade.
#
# 	r = requests.get(URL + "/pubticker/" + symbol, verify=True) # <== UPDATED TO LATEST VERSION OF BFX!
# 	rep = r.json()
#
# 	try:
# 		rep['last_price']
# 	except KeyError:
# 		return rep['message']
#
# 	return rep
#
# result = ticker
# print(result)

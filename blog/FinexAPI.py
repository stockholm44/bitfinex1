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

a = [1,2,3,4,5]
b = [8,7,6,5,4]
print(a)
print(b)
c = a + b
print(c)
# def symbol_list():
# 	URL = "https://api.bitfinex.com/v1/symbols"
# 	response = requests.request("GET", URL)
# 	rep = response.json()
# 	return rep

def symbol_list():
	symbols = {}
	symbols_1 = ('btcusd', 'ethusd', 'eosusd', 'xrpusd', 'iotusd', 'bchusd', 'neousd', 'qtmusd')
	symbols_2 =('BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM')
	a = len(symbols_1)
	b = len(symbols_2)
	# for symbol_1 in symbols_1:
	# 	for symbol_2 in symbols_2:
	# 		symbols[symbol_1] = symbol_2
	for i in range(a-1):
		symbols[symbols_2[i]] = symbols_1[i]


	# ('rrtusd', 'rrtbtc', 'zecusd', 'zecbtc', 'xmrusd', 'xmrbtc', 'dshusd', 'dshbtc', 'btceur', 'btcjpy', 'xrpusd', 'xrpbtc', 'iotusd', 'iotbtc', 'ioteth', 'eosusd', 'eosbtc')

	# ('eoseth', 'sanusd', 'sanbtc', 'saneth', 'omgusd', 'omgbtc', 'omgeth', 'bchusd', 'bchbtc', 'bcheth', 'neousd', 'neobtc', 'neoeth', 'etpusd', 'etpbtc', 'etpeth', 'qtmusd', 'qtmbtc', 'qtmeth', 'avtusd', 'avtbtc', 'avteth', 'edousd', 'edobtc', 'edoeth', 'btgusd', 'btgbtc', 'datusd', 'datbtc', 'dateth', 'qshusd', 'qshbtc', 'qsheth', 'yywusd', 'yywbtc', 'yyweth', 'gntusd', 'gntbtc', 'gnteth', 'sntusd', 'sntbtc', 'snteth', 'ioteur', 'batusd', 'batbtc', 'bateth', 'mnausd', 'mnabtc', 'mnaeth', 'funusd', 'funbtc', 'funeth', 'zrxusd', 'zrxbtc', 'zrxeth', 'tnbusd', 'tnbbtc', 'tnbeth', 'spkusd', 'spkbtc', 'spketh', 'trxusd', 'trxbtc', 'trxeth', 'rcnusd', 'rcnbtc', 'rcneth', 'rlcusd', 'rlcbtc', 'rlceth', 'aidusd', 'aidbtc', 'aideth', 'sngusd', 'sngbtc', 'sngeth', 'repusd', 'repbtc', 'repeth', 'elfusd', 'elfbtc', 'elfeth', 'btcgbp', 'etheur', 'ethjpy', 'ethgbp', 'neoeur', 'neojpy', 'neogbp', 'eoseur', 'eosjpy', 'eosgbp', 'iotjpy', 'iotgbp', 'iosusd', 'iosbtc', 'ioseth', 'aiousd', 'aiobtc', 'aioeth', 'requsd', 'reqbtc', 'reqeth', 'rdnusd', 'rdnbtc', 'rdneth', 'lrcusd', 'lrcbtc', 'lrceth', 'waxusd', 'waxbtc', 'waxeth', 'daiusd', 'daibtc', 'daieth', 'cfiusd', 'cfibtc', 'cfieth', 'agiusd', 'agibtc', 'agieth', 'bftusd', 'bftbtc', 'bfteth', 'mtnusd', 'mtnbtc', 'mtneth', 'odeusd', 'odebtc', 'odeeth')
	return symbols

# a = symbol_list()
# b = list(a.keys())
# print(b)
# Bithumb API
def bid_bithumb(symbol):
	URL = "https://api.bithumb.com/public/ticker/%s" % symbol
	response = requests.request("GET", URL)
	rep = response.json()
	data = rep['data']
	bid = data['closing_price']
	return bid

def symbol_list_bithumb():
	symbols = ('BTC','ETH','EOS','XRP','BCH','QTUM')
	return symbols

# a = bid_bithumb('BTC')
# print(a)
# symbols = symbol_list()
# coin_price = {}
# for symbol in symbols:
#     coin_price[symbol] = bid_Finex(symbol)
#
# print(coin_price)


# a= symbol_list()
# print(a)
# print(a[1])
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

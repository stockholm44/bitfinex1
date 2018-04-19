from django.utils import timezone
# from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
# from .forms import PostForm
from django.http import HttpResponse, JsonResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from FinexAPI import *
from django.views.decorators.csrf import csrf_exempt

#
# def keyboard(request):
#
#     return JsonResponse({
#         'type' : 'buttons',
#         'buttons' : ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
#     })
# @csrf_exempt
# # def message(request):
def message():
    symbol_list_bitfinex = symbol_list()
    symbol_list_bithumb = ['BTC','ETH','EOS','XRP','BCH','QTUM']
    #원래는 FinexAPI()에서 list를 return 할려고 했는데 계속 지역에러가 떠서 그냥 리스트를 함수내에서 정의함.ㅜㅜ
    symbol_list_keys = list(symbol_list().keys())

    symbol_list_total = symbol_list_keys + symbol_list_bithumb
    # print(symbol_list_total)
    # json_str = ((request.body).decode('utf-8'))
    # received_json_data = json.loads(json_str)
    # data = rec    eived_json_data['content']
    data = 'QTUM'

    if data in symbol_list_keys:
            symbol_1 = data
            symbol = symbol_list_bitfinex[symbol_1]
            price_usd = bid_Finex(symbol)
            price_usd = format(int(price_usd),',')
    if data in symbol_list_bithumb:
            symbol = data
            price_krw = bid_bithumb(symbol)
            price_krw = int(price_krw)
            price_krw = format(int(price_krw),',')

    today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    if data in symbol_list_keys and data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)
    elif data in symbol_list_keys:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd)
    elif data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)

    response_message = str(response_1)

    if data in symbol_list_total:
        return response_1
    else:
        return "This is not coin."
        # return JsonResponse({
        #         "message": {
        #             "text": response_message
        #         },
        #         "keyboard": {
        #             "type": "buttons",
        #             "buttons": ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
        #         }
        #
        #     })

def message1():
    symbol_list_bitfinex = symbol_list()
    symbol_list_bithumb = ['BTC','ETH','EOS','XRP','BCH','QTUM']
    #원래는 FinexAPI()에서 list를 return 할려고 했는데 계속 지역에러가 떠서 그냥 리스트를 함수내에서 정의함.ㅜㅜ
    symbol_list_keys = list(symbol_list().keys())

    # symbol_list_total = symbol_list_keys + symbol_list_bithumb
    # json_str = ((request.body).decode('utf-8'))
    # received_json_data = json.loads(json_str)
    # data = received_json_data['content']

    data = input("입력해")

    if data in symbol_list_keys:
            symbol_1 = data
            symbol = symbol_list_bitfinex[symbol_1]
            price_usd = bid_Finex(symbol)
            price_usd = float(price_usd)
            price_usd = format(price_usd,',')
    if data in symbol_list_bithumb:
            symbol = data
            price_krw = bid_bithumb(symbol)
            price_krw = int(price_krw)
            price_krw = format(price_krw,',')

    today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    if data in symbol_list_keys and data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)
    elif data in symbol_list_keys:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd)
    elif data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)

    return response_1

    # if data in symbol_list_total:
    #     return JsonResponse({
    #             "message": {
    #                 "text": response_message
    #             },
    #             "keyboard": {
    #                 "type": "buttons",
    #                 "buttons": ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
    #             }
    #
    #         })
    # else:
    #     return JsonResponse({
    #             'message': {
    #                 'text': '알라카솜~~~'
    #             },
    #             'keyboard': {
    #                 'type': 'buttons',
    #                 'buttons': ['BTC', 'ETH', 'XRP']
    #             }
    #
    #         })

# a = message()
# print(a)
# b = 10000
# c = format(10000,',')
# print(c)
# print(type(c))
# price = 10000

a = message1()
print(a)

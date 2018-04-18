# from django.utils import timezone
# from .models import Post
# from django.shortcuts import render, get_object_or_404, redirect
# from .forms import PostForm
from django.http import HttpResponse, JsonResponse
import datetime
# from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from FinexAPI import *
from django.views.decorators.csrf import csrf_exempt


# def current_datetime(request):
#     now = datetime.datetime.now()
#     return render(request, 'current_datetime.html',{'current_time': now})
# def hours_ahead(request, offset):
#     try:
#          offset=int(offset)
#     except ValueError:
#         raise Http404()
#     dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
#     html = "<html><body>In %s times, it will be %s.</body></html)" % (offset,dt)
#     return HttpResponse(html)
# def hello(request):
#     return HttpResponse("Hello world")
def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
    })
@csrf_exempt
def message(request):
    symbol_list = list(symbol_list().keys())
    symbol_list_bitfinex = symbol_list()
    symbol_list_bithumb = symbol_list_bithumb()
    symbol_list_total = symbol_list + symbol_list_bithumb
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    data = received_json_data['content']
    if data in symbol_list:
            symbol_1 = data
            symbol = symbol_list_bitfinex[symbol_1]
            price_usd = bid_Finex(symbol)
            # price_won = format(price,',')
    if data in symbol_list_bithumb:
            symbol = data
            price_krw = bid_bithumb(symbol)

    today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    if data in symbol_list and data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)
    elif data in symbol_list:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd)
    elif data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " KRW in Bitthumb : " + str(price_krw)

    response_message = str(response_1)

    if data in symbol_list_total:
        return JsonResponse({
                "message": {
                    "text": response_message
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
                }

            })



    # return JsonResponse({
    #         'message': {
    #             'text': today_date + '의 ' + data + '시세는 ' + price +' 입니다.'
    #         },
    #         'keyboard': {
    #             'type': 'buttons',
    #             'buttons': ['BTC', 'ETH', 'XRP']
    #         }
    #
    #     })



# Test
symbol_list_keys = list(symbol_list().keys())
print(symbol_list_keys)
symbol_list_bitfinex = symbol_list()
print(symbol_list_bitfinex)
symbol_list_bithumb = symbol_list_bithumb()
print(symbol_list_bithumb)
symbol_list_total = symbol_list_keys + symbol_list_bithumb
print(symbol_list_total)
json_str = ((request.body).decode('utf-8'))
received_json_data = json.loads(json_str)
data = received_json_data['content']
if data in symbol_list_keys:
        symbol_1 = data
        symbol = symbol_list_bitfinex[symbol_1]
        price_usd = bid_Finex(symbol)
        print(price_usd)
        # price_won = format(price,',')
if data in symbol_list_bithumb:
        symbol = data
        price_krw = bid_bithumb(symbol)

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
    JsonResponse({
            "message": {
                "text": response_message
            },
            "keyboard": {
                "type": "buttons",
                "buttons": ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
            }

        })
    print(JsonResponse)

from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from blog.FinexAPI import *
from blog.cmc import *
from blog.scrap import *
from blog.bab import *
from blog.coin_index import *
from django.views.decorators.csrf import csrf_exempt
import json
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup

def keyboard(request):
    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP', 'JPY_Exchange']
    })

@csrf_exempt
def message(request):

    # Kakao 플러스친구에서의 input Data
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    data = received_json_data['content']    # 카카오 플러스친구가 받는 input 값.

    # 전체적으로 1. 밥뭐먹지 2.코인순위(10,20,50단위) 3. 개별코인정보(BTC,ETH,XRP)
    # response_message를 만들기 전까지 준비데이터들을 아래와 같이 만든다.

    # 조건문으로 계산 최소화를 해보자.(data 입력값에 따라 다른 입력값들에 따른 계산들을 하지말자.)
    bab_place = bab_place_list() # 1번용 Data 범위
    coin_list_top3 = ['BTC', 'ETH', 'XRP']  # 3번 용 Data 범위


    #1. 밥 뭐먹지
    if data in bab_place:
        bab_response = bab(data)


        # 10위만 남기고 지움. 백업용으로 주석으로 남김.
        # coin_rate_selector = ['Coin_Rank_Top 5', 'Coin_Rank_Top 10','Coin_Rank_Top 20']
        #
        # if data == 'Coin_Rank_Top 5':
        #     coin_count = 5
        # elif data == 'Coin_Rank_Top 10':
        #     coin_count = 10
        # elif data == 'Coin_Rank_Top 20':
        #     coin_count = 20
        # else:
        #     coin_count = 0

        # coinmarketcap 에서 Data 끌어오기.

    # 2. 코인순위의 Data
    # 원하는 코인순위 범위 정하기
    elif data == 'Coin_Rank_Top 10':
        coin_count = 10
        coin_data = ticker1(coin_count)


    # 2. 코인순위의 response_message
        response_message = ""
        for i in range(coin_count):
            rank = int(coin_data[i]['rank'])
            name = coin_data[i]['name']
            price_usd = float(coin_data[i]['price_usd']) # float
            price_krw = float(coin_data[i]['price_krw']) # float
            str_price_usd = format(float(coin_data[i]['price_usd']),',.2f') # str_1000단위 + 소수점2자리
            str_price_krw = format(float(coin_data[i]['price_krw']),',.0f') # str_1000단위 + 소수점 0자리
            percent_change_24h = format(float(coin_data[i]['percent_change_24h']),'.2f')
            gimp = format(((1-price_krw/price_usd/1077)*100), '.2f')
            if float(percent_change_24h) > 0:
                change_mark = '▲'
                add_change_mark = '+'
            elif float(percent_change_24h) == 0:
                change_mark = ''
                add_change_mark = ''
            elif float(percent_change_24h) < 0:
                change_mark = '▼'
                add_change_mark = ''

            volume_usd = float(coin_data[i]['24h_volume_usd'])
            available_supply = float(coin_data[i]['available_supply'])
        # 회전율
            circul_rate = format(float(volume_usd/available_supply/float(price_usd)*100),'.2f')

        # 2. 코인순위의 message_response
            message_this_coin = str(rank) + '위\n┌ ' + name +'   '+ str_price_usd +'$/' + str_price_krw + '원\n├ 김프    ' + gimp + '%\n├ 변화율   ' + add_change_mark + percent_change_24h + "% (" +change_mark + ')\n└ 회전율   ' + circul_rate + '%\n---------------------\n'
            response_message += message_this_coin

    # 3. 기타 코인관련 잡기능 BTC, ETH, XRP 들의 개별 dATA + 잡 코멘트 넣기.

    elif data in coin_list_top3:
        coin_data = ticker2(data)[0]
        rank = int(coin_data['rank'])
        name = coin_data['name']
        price_usd = float(coin_data['price_usd']) # float
        price_krw = float(coin_data['price_krw']) # float
        str_price_usd = format(float(coin_data['price_usd']),',.2f') # str_1000단위 + 소수점2자리
        str_price_krw = format(float(coin_data['price_krw']),',.0f') # str_1000단위 + 소수점 0자리
        percent_change_24h = format(float(coin_data['percent_change_24h']),'.2f')
        gimp = format(((1-price_krw/price_usd/1077)*100), '.2f')
        if float(percent_change_24h) > 0:
            change_mark = '▲'
            add_change_mark = '+'
        elif float(percent_change_24h) == 0:
            change_mark = ''
            add_change_mark = ''
        elif float(percent_change_24h) < 0:
            change_mark = '▼'
            add_change_mark = ''
        volume_usd = float(coin_data['24h_volume_usd'])
        available_supply = float(coin_data['available_supply'])
    # 회전율
        circul_rate = format(float(volume_usd/available_supply/float(price_usd)*100),'.2f')

        response_message = str(rank) + '위\n┌ ' + name +'   '+ str_price_usd +'$/' + str_price_krw + '원\n├ 김프    ' + gimp + '%\n├ 변화율   ' + add_change_mark + percent_change_24h + "% (" +change_mark + ')\n└ 회전율   ' + circul_rate + '%\n---------------------\n'
        if data == 'BTC':
            message_this_coin = '\n 기축코인 비트코인 떡락 ㄱ ㄱ\n\n'
            time_delta_list, time_delta_list_name, rsi_value_list = rsi_btc_values()
            for i, line in enumerate(time_delta_list):
                message_this_coin += time_delta_list_name[i] +'분봉 : ' + 'rsi = ' + str(rsi_value_list[i]) + '\n'
        elif data == 'ETH':
            cym_ETH = 20.86 /3 * price_krw
            cym_ETH = int(cym_ETH)
            cym_ETH_Ratio = cym_ETH / 5000000 * 100
            cym_ETH_gap = cym_ETH-5000000
            cym_ETH_Ratio = float(cym_ETH_Ratio)

            if cym_ETH_gap > 0:
                plusminus = "아직은 이익이다.^^ " + format(cym_ETH_gap, ',') + "원 이익이다! \n●●●●●●●●●●●●●●●●●●●●\n18,000원 치킨 ▶" + str(int(cym_ETH_gap/18000)) + "마리◀를 쳐먹을 수 있다. \n\n●●●● 쏘리 지이이일럿!!!!●●●●\n\n●●●아이라이포 아이어!!!!●●●"
            elif cym_ETH_gap < 0:
                plusminus = "아직은 꼴아있다. ㅜㅜ"
            elif cym_ETH_gap == 0:
                plusminus = "똔똔이다.ㅡㅡ"

            cym_ETH_Ratio_str = format(cym_ETH_Ratio, '.1f')
            cym_ETH = format(cym_ETH, ',')
            cym_ETH_gap = format(cym_ETH_gap, ',')

            message_this_coin = "\n★★★★★★★★★★★★★★★★★★\n현재 심봉&진우의 ETH는 각각\n" + str(cym_ETH) + "원이다 십생키들아.\n" + "즉 초기 대비 현재 " + cym_ETH_Ratio_str + "% 인것이다.\n그래서 현재 투자 결과는 " + plusminus
        elif data =='XRP':
            message_this_coin = "\n★★★★★★★★★★★★★★★\n심재리플 리플심재"

    # 4. JPY Exchange_Rates List 보이기 + 최저가격 보여주기
    elif data == 'JPY_Exchange':
        response_message_jpy = jpy_rate_kakao()
        # response_message_jpy = jpy_test2()
        # aa, bb = jpy_test2()
        # cc = aa[0]



    # today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    # 최종 결과 : 카카오톡 플러스로 보내는 output
    if data == "JPY_Exchange":
        return JsonResponse({
                "message": {
                    "text": response_message_jpy
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP','JPY_Exchange']
                }

                })
    elif data == 'Coin_Rank_Top 10':
        return JsonResponse({
                "message": {
                    "text": response_message
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP','JPY_Exchange']
                }

                })
    elif data == '지금 뭐먹지?':
        return JsonResponse({
                "message": {
                    "text": "지역을 선택해주십시오.\n★★★★★★★★★★★★★\n0. 파주\n1. 고양\n2. 서울\n★★★★★★★★★★★★★"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['파주','고양','서울']
                }

                })
    elif data in bab_place:
        return JsonResponse({
                "message": {
                    "text": bab_response
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP','JPY_Exchange']
                }

                })
    elif data == "파주":
        return JsonResponse({
                "message": {
                    "text": "상세지역을 선택해 주십숑.\n★★★★★★★★★★★★★\n1. 파주 P8공장뒤\n2. 파주 LGD기숙사뒤\n3. 파주 내 그외지역\n★★★★★★★★★★★★★"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['파주 P8공장뒤','파주 LGD기숙사뒤','파주 내 그외지역']
                }

                })
    elif data == "서울":
        return JsonResponse({
                "message": {
                    "text": "상세지역을 선택해 주십숑.\n★★★★★★★★★★★★★\n1. 홍대\n2. 연희동\n★★★★★★★★★★★★★"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['연희동','홍대']
                }

                })
    elif data == "고양":
        return JsonResponse({
                "message": {
                    "text": "상세지역을 선택해 주십숑.\n★★★★★★★★★★★★★\n1. 화정\n2. 일산\n3. 관산동\n★★★★★★★★★★★★★"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['화정','일산','관산동']
                }

                })
    elif data in coin_list_top3:
        return JsonResponse({
                "message": {
                    "text": response_message + message_this_coin
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP','JPY_Exchange']
                }

                })
    else:
        return JsonResponse({
                "message": {
                    "text": "뭘쳐누른거냐."
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['지금 뭐먹지?','Coin_Rank_Top 10','BTC', 'ETH', 'XRP','JPY_Exchange']
                }

                })

def price_coin(request):
    symbol_list_bitfinex = symbol_list()
    symbol_list_keys = list(symbol_list().keys())
    symbols = symbol_list()
    coin_price = {}
    for symbol in symbol_list_keys:
        symbol_1 = symbol
        symbol_2 = symbol_list_bitfinex[symbol_1]
        coin_price[symbol_2] = bid_Finex(symbol_2)
    # coin_price = sorted(coin_price.item)
    # coin_price['gimp'] = gimp()
    symbols_bithumb = symbol_list_bithumb()
    coin_price_bithumb = {}
    for symbol in symbols_bithumb:
        coin_price_bithumb[symbol] = bid_bithumb(symbol)
    # coin_price_bithumb = sorted(coin_price_bithumb.item)
    # gimp = gimp()
    # context = {'coin_price': coin_price, 'volume': volume, 'gimp':gimp}

    context = {'coin_price': coin_price, 'coin_price_bithumb': coin_price_bithumb}
    return render(request, 'blog/price_coin.html', context)
    # return HttpResponse("BTC is %d$" % volume)

def rsi_list(request):
    start_time = time.time()
    # 180519_BTC의 time봉별 RSI리스트 dict화
    time_delta_list, time_delta_list_name, rsi_btc_value_list = rsi_btc_values()
    rsi_btc_list = {}
    for i, time_delta in enumerate(time_delta_list_name):
        rsi_btc_list[time_delta] = rsi_btc_value_list[i]

    # 180519_Coin별 1일봉 RSI리스트 dict화
    symbols, rsi_coin_value_list = rsi_coin_values()
    rsi_coin_list = {}
    for i, symbol_temp in enumerate(symbols):
        rsi_coin_list[symbol_temp] = rsi_coin_value_list[i]

    end_time = time.time()
    elapse_time = int(end_time - start_time)
    if elapse_time > 20:
        elapse_time_message = 'Loading이 너무 오래걸렸습니다. 코딩 최적화가 절실합니다.'
    elif elapse_time > 10:
        elapse_time_message = 'Loading이 좀 걸렸습니다. 조금 수정이 필요합니다.'
    else:
        elapse_time_message = 'Loading이 적당합니다. 냅둬도됩니다.'

    context = {'rsi_btc_list': rsi_btc_list,'rsi_coin_list': rsi_coin_list,'elapse_time':elapse_time,
               'elapse_time_message':elapse_time_message}

    return render(request, 'blog/rsi_list.html', context)

def jpy_list(request):
    start_time = time.time()
    minimum_rate, minimum_rate_exchange = jpy_rate_min()
    bank_name, bank_exchange_rate = jpy_rate()
    jpy_exchange_list = {}
    for i in range(len(bank_name)):
        jpy_exchange_list[bank_name[i]] = bank_exchange_rate[i]

    end_time = time.time()
    elapse_time = int(end_time - start_time)
    if elapse_time > 20:
        elapse_time_message = 'Loading이 너무 오래걸렸습니다. 코딩 최적화가 절실합니다.'
    elif elapse_time > 10:
        elapse_time_message = 'Loading이 좀 걸렸습니다. 조금 수정이 필요합니다.'
    else:
        elapse_time_message = 'Loading이 적당합니다. 냅둬도됩니다.'

    context = {
        'minimum_rate': minimum_rate,
        'minimum_rate_exchange': minimum_rate_exchange,
        'jpy_exchange_list': jpy_exchange_list,
        'elapse_time':elapse_time,
        'elapse_time_message':elapse_time_message
        }
    return render(request, 'blog/jpy_list.html', context)


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
def index(request):
    person= {'firstname': 'Craig', 'lastname': 'Daniels'}
    weather= "sunny"
    context= {
        'person': person,
        'weather': weather,
        }
    return render(request, 'blog/post_list.html', context)

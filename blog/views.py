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
from django.views.decorators.csrf import csrf_exempt
import json
import random

def keyboard(request):
    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['Bab?','Coin_Rank_Top 10', 'Coin_Rank_Top 20','Coin_Rank_Top 50','BTC', 'ETH', 'XRP']
    })

@csrf_exempt
def message(request):

    # Kakao 플러스친구에서의 input Data
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    data = received_json_data['content']    # 카카오 플러스친구가 받는 input 값.

    # 전체적으로 1. 밥뭐먹지 2.코인순위(10,20,50단위) 3. 개별코인정보(BTC,ETH,XRP)
    # response_message를 만들기 전까지 준비데이터들을 아래와 같이 만든다.

    # 1. 밥뭐먹지의 Data
    if data == "Bab?":
        bab_list = ['볶음밥','짜장면','짬뽕','간짜장','양념치킨','걍치킨','순살치킨','신라면','진라면','컵라면큰사발','컵라면','불닭볶음밥','굶어시바라','닭도리탕','새우깡','보쌈','고르곤졸라피자','불고기피자','김치에계란','계란말이','회','스시','초밥','간장게장','양념게장']
        bab_select = random.choice(bab_list)

    # 2. 코인순위의 Data
    # 원하는 코인순위 범위 정하기
    coin_rate_selector = ['Coin_Rank_Top 10', 'Coin_Rank_Top 20','Coin_Rank_Top 50']

    if data == 'Coin_Rank_Top 10':
        coin_count = 9
    elif data == 'Coin_Rank_Top 20':
        coin_coint = 19
    elif data == 'Coin_Rank_Top 50':
        coin_count = 49
    else:
        coin_count = 0

    # coinmarketcap 에서 Data 끌어오기.
    coin_data = ticker(coin_count)

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
        if float(percent_change_24h) > 0:
            change_mark = '▲'
            add_change_mark = '+'
        elif float(percent_change_24h) == 0:
            change_mark = '-'
            add_change_mark = ''
        elif float(percent_change_24h) < 0:
            change_mark = '▼'
            add_change_mark = ''

        volume_usd = float(coin_data[i]['24h_volume_usd'])
        available_supply = float(coin_data[i]['available_supply'])
        # 회전율
        circul_rate = format(float(volume_usd/available_supply/float(price_usd)*100),'.2f')
        message_this_coin = str(rank) + '위: ' + name +' - '+ str_price_usd +'$/' + str_price_krw + '원 (' + change_mark + percent_change_24h + change_mark + ') - 회전율:' + circul_rate + '%\n'

        response_message += message_this_coin
        response_1 = str(response_message)



    today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    if data in coin_rate_selector:
        return JsonResponse({
                "message": {
                    "text": response_1
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['Bab?','Coin_Rank_Top 10', 'Coin_Rank_Top 20','Coin_Rank_Top 50','BTC', 'ETH', 'XRP']
                }

            })
    elif data == "Bab?":
        return JsonResponse({
                "message": {
                    "text": "오늘 먹을 식사는 아래와 같습니다.\n★★★★★★★★★★★★★\n" + bab_select + "\n★★★★★★★★★★★★★"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['Bab?','Coin_Rank_Top 10', 'Coin_Rank_Top 20','Coin_Rank_Top 50','BTC', 'ETH', 'XRP']
                }

            })








    #
    # if data == "ETH":
    #         cym_ETH = 20.86 * int(bid_bithumb("ETH"))/3
    #         cym_ETH = int(cym_ETH)
    #         cym_ETH_Ratio = cym_ETH / 5000000 * 100
    #         cym_ETH_gap = cym_ETH-5000000
    #         cym_ETH_Ratio = float(cym_ETH_Ratio)
    #
    #         if cym_ETH_gap > 0:
    #             plusminus = "이익이다.^^"
    #         elif cym_ETH_gap < 0:
    #             plusminus = "꼴았다. ㅜㅜ"
    #         elif cym_ETH_gap == 0:
    #             plusminus = "똔똔이다.ㅡㅡ"
    #
    #         cym_ETH_Ratio = format(cym_ETH_Ratio, '.1f')
    #         cym_ETH = format(cym_ETH, ',')
    #         cym_ETH_gap = format(cym_ETH_gap, ',')


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

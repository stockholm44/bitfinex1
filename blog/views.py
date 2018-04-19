from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from blog.FinexAPI import *
from django.views.decorators.csrf import csrf_exempt
import json

def keyboard(request):

    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
    })
@csrf_exempt
# def message(request):
def message(request):
    symbol_list_bitfinex = symbol_list()
    symbol_list_bithumb = ['BTC','ETH','EOS','XRP','BCH','QTUM']
    #원래는 FinexAPI()에서 list를 return 할려고 했는데 계속 지역에러가 떠서 그냥 리스트를 함수내에서 정의함.ㅜㅜ
    symbol_list_keys = list(symbol_list().keys())

    symbol_list_total = symbol_list_keys + symbol_list_bithumb
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    data = received_json_data['content']

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
    if data == "ETH":
            cym_ETH = 20.86 * int(bid_bithumb("ETH"))/3
            cym_ETH = int(cym_ETH)
            cym_ETH_Ratio = cym_ETH / 5000000 * 100
            cym_ETH_gap = 5000000-cym_ETH
            cym_ETH_Ratio = float(cym_ETH_Ratio)

            if cym_ETH_gap > 0:
                plusminus = "이익이다.^^"
            elif cym_ETH_gap < 0:
                plusminus = "꼴았다. ㅜㅜ"
            elif cym_ETH_gap == 0:
                plusminus = "똔똔이다.ㅡㅡ"

            cym_ETH_Ratio = format(cym_ETH_Ratio, '.1f')
            cym_ETH = format(cym_ETH, ',')
            cym_ETH_gap = format(cym_ETH_gap, ',')




    # if data in symbol_list_keys and data in symbol_list_bithumb:
    #         gimp = float(price_krw)/ float(price_usd) / 1096 * 100


    today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # today_date = datetime.date.today().strftime("%m월 %d일")

    if data in symbol_list_keys and data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "$\n" + str(data) + " KRW in Bitthumb : " + str(price_krw) + "원"
    elif data in symbol_list_keys:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "$"
    elif data in symbol_list_bithumb:
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " KRW in Bitthumb : " + str(price_krw) + "원"

    if data == "ETH":
        response_1 = str(today_date) + " 의 시세\n" + str(data) + " USD in Bitfinex : " + str(price_usd) + "\n" + str(data) + " KRW in Bitthumb : " + str(price_krw) + "\n★★★★★★★★★★★★★★★★★★\n현재 심봉&진우의 ETH는 각각\n" + str(cym_ETH) + "원이다 십생키들아.\n" + "즉 초기 대비 현재 " + cym_ETH_Ratio + "% 인것이다.\n그래서 현재 투자 결과는 " + plusminus
    elif data == "XRP":
        response_1 += "\n★★★★★★★★★★★★★★★\n심재리플 리플심재"

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
    else:
        return JsonResponse({
                "message": {
                    "text": "알라카솜."
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
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

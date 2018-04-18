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
        'buttons' : ['BTC', 'ETH', 'XRP', 'VAR']
    })
@csrf_exempt
def message(request):
    # symbol_list = ['BTC', 'ETH', 'XRP']
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    data = received_json_data['content']
    # if data in symbol_list:
    #         symbol = data
    #         price = bid_bithumb(symbol)
    today_date = datetime.date.today().strftime("%m월 %d일")
    response_1 = str(today_date) + "의 " + stt(data) + "시세는 " + str(price) +" 입니다."
    response_message = str(response_1)
    if data =="BTC":
        return JsonResponse({
                "message": {
                    "text": "BTC가격??? 몰라이이십새야"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'XRP', 'VAR']
                }

            })
    elif data == "ETH":
        return JsonResponse({
                "message": {
                    "text": "ETH 가격??? 몰라이 십새야. 비탈릭 십세"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'XRP', 'VAR']
                }

            })
    elif data == "XRP":
        return JsonResponse({
                "message": {
                    "text": response_message
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'XRP', 'VAR']
                }

            })
    elif data == "VAR":
        return JsonResponse({
                "message": {
                    "text": 11 + 12
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'XRP', 'VAR']
                }

            })
    else:
        return JsonResponse({
                "message": {
                    "text": "개놈의 새끼"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['BTC', 'ETH', 'XRP', 'VAR']
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
def price_coin(request):
    symbols = symbol_list()
    coin_price = {}
    for symbol in symbols:
        coin_price[symbol] = bid_Finex(symbol)
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

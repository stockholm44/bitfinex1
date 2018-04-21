from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from blog.FinexAPI import *
from django.views.decorators.csrf import csrf_exempt
import json
import random

@csrf_exempt
def message(request): 구버전.
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
            cym_ETH_gap = cym_ETH-5000000
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

    if data == "밥뭐먹지?":
        bab_list = ['볶음밥','짜장면','짬뽕','간짜장','양념치킨','걍치킨','순살치킨','신라면','진라면','컵라면큰사발','컵라면','불닭볶음밥','굶어시바라','닭도리탕','새우깡','보쌈','고르곤졸라피자','불고기피자','김치에계란','계란말이','회','스시','초밥','간장게장','양념게장']
        bab_select = random.choice(bab_list)


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

    if data == "밥뭐먹지?":
        response_1 = "오늘 먹을 식사는 아래와 같습니다.\n★★★★★★★★★★★★★\n" + bab_select + "\n★★★★★★★★★★★★★"

    response_message = str(response_1)

    if data in symbol_list_total:
        return JsonResponse({
                "message": {
                    "text": response_message
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['밥뭐먹지?','BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
                }

            })
    elif data == "밥뭐먹지?":
        return JsonResponse({
                "message": {
                    "text": response_message
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['밥뭐먹지?','BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
                }

            })
    else:
        return JsonResponse({
                "message": {
                    "text": "알라카쏨~~~"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": ['밥뭐먹지?','BTC', 'ETH', 'EOS', 'XRP', 'IOTA', 'BCH', 'NEO', 'QTUM']
                }

            })

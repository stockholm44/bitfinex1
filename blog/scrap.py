from bs4 import BeautifulSoup
from urllib.request import urlopen

__all__ = ['jpy_rate','jpy_rate_list','jpy_test']

def jpy_rate():
    html = urlopen('https://www.mibank.me/exchange/saving/index.php?currency=JPY')
    # html = urlopen('https://coinmarketcap.com/')
    source = html.read()
    html.close()

    soup = BeautifulSoup(source, "html.parser")

    # 1. 환전소 이름찾기
    table_div = soup.find("div",{"class": "box_contents1"})
    spans = table_div.find_all("span",{'class':'bank_name'})
    bank_name = []
    for a_tag in spans:
        bank_name.append(a_tag.text)

    # for i, name in enumerate(bank_name):
    #     print(i, name)


    # 2. 환전소의 환전 가격만 뽑기
    tbody_div = soup.find_all('tbody')
    # print(tbody_div)
    tr_tag = tbody_div[1].find_all('tr')
    # print(tr_tag)
    # print(len(tr_tag))
    # for i in range(len(tr_tag)):
    #     a = tr_tag[i].find_all('td',{'class':'right txt_em '})

    bank_exchange_rate = []
    for i in range(len(tr_tag)):
        if i == 0:
            a = tr_tag[i].find_all('td',{'class':'right txt_em box'})
            # print(a)
            exchange_rates = a[0].text.split('원')
            bank_exchange_rate.append(exchange_rates[0])
        elif i > 0:
            a = tr_tag[i].find_all('td',{'class':'right txt_em '})
            # print(a)
            exchange_rates = a[0].text.split('원')
            bank_exchange_rate.append(exchange_rates[0])
    bank_exchange_rate = bank_exchange_rate[:len(bank_name)]
    # for i, rate in enumerate(bank_exchange_rate):
    #     print(i, rate)

    return bank_name, bank_exchange_rate

def jpy_rate_list():
    # 4. JPY Exchange_Rates List 보이기 + 최저가격 보여주기
    bank_name, bank_exchange_rate = jpy_rate()
    response_message = ""
    # 제일 싼 거래소 보여주기
    minimum_rate = bank_exchange_rate[0]    # 비교 하기 위한 제일 싼 환율
    minimum_rate_exchange = bank_name[0]              # 싼거래소들
    for i in range(len(bank_name)):
        if i > 0:
            if bank_exchange_rate[i] == minimum_rate:
                minimum_rate_exchange += ", " + bank_name[i]

    response_message += '★★★★★★★★★★★★★\n제일 저렴한 환율은 ' + str(minimum_rate) + '엔 이며 저렴한 거래소는 아래거래소들 입니다.\n' + minimum_rate_exchange + '\n★★★★★★★★★★★★★\n'
    message_this_rate = ""
    for i, name in enumerate(bank_name):
        message_this_rate += str(i + 1) + '. ' + name + ': ' + str(bank_exchange_rate[i]) + '엔\n'

    response_message += message_this_rate

    # return "SSORI ZEALOT!!!!!!!!!!!!!"
    return response_message
def jpy_test2():
    a = ['aa','bb','cc']
    b = ['dd','ee','ff']
    return a, b
def jpy_test():
    bank_name, bank_exchange_rate = jpy_test2()
    a = bank_name[0]
    b = bank_exchange_rate[0]
    c = a + b
    return c

aa, bb = jpy_test2()
cc = aa[0]
print(cc)
# d ,e = jpy_rate()
# # f = jpy_rate_list()
# g = jpy_test()
# print(g)
# print(d)
# print(e)
# print(f)
# print(g)

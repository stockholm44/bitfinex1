from bs4 import BeautifulSoup
from urllib.request import urlopen

__all__ = ['jpy_rate']

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

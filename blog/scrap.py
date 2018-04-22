from bs4 import BeautifulSoup
from urllib.request import urlopen

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

print(bank_name)


# 2. 환전소의 환전 가격만 뽑기
tbody_div = soup.find_all('tbody')
tr_tag = tbody_div[1].find_all('tr')

# for i in range(len(tr_tag)):
#     a = tr_tag[i].find_all('td',{'class':'right txt_em '})
bank_exchange_rate = []
for i in range(len(tr_tag)):
    if i > 0:
        a = tr_tag[i].find_all('td',{'class':'right txt_em '})
        exchange_rates = a[0].text.split('원')
        bank_exchange_rate.append(exchange_rates[0])

print(bank_exchange_rate)
print(len(bank_name))
print(len(bank_exchange_rate))

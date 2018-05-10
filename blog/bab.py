import random

__all__ = ['bab']

def bab(data):
    if data == '화정':
        bab_list = {'농부치킨': 'http://naver.me/Gfpkc3HS',
                    '민쿡다시마':'http://naver.me/FSCbE0x5',
                    '동산손만두': 'http://naver.me/xk0XUyeq'}
    elif data == '일산':
        bab_list = {'보릿고개': 'http://naver.me/GyfrMDlC',
                    '양천리 양꼬치':'http://naver.me/5BYRCB05'}
    elif data == '관산동':
        bab_list = {'한우천국': 'http://naver.me/5eVPiR4M',
                    '더더 간장게장':'http://naver.me/GQp5AjcQ'}
    elif data == '연희동':
        bab_list = {'카덴': 'http://naver.me/5AJZ5kvy',
                    '스시마쯔':'http://naver.me/Fg6Ix2Z8',
                    '서백자와 허규일':'http://naver.me/FDBSx629',
                    '여우골':'http://naver.me/FObKEqBE'}
    elif data == '홍대':
        bab_list = {'김진환제과점': 'http://naver.me/5AJ8cWMj',
                    '레게치킨':'http://naver.me/Gzu2VkIm',
                    '국시집':'http://naver.me/5CE48jmL'}

        bab_select = random.choice(list(bab_list.items()))
    bab_response = data + ' 지역에서 고를수 있는 ♥랜덤맛집♥은 다음과 같습니다.\n★★★★★★★★★★★★★\n\n●●● 맛집이름 : ' + bab_select[0] + '\n네이버 지도 링크 ↓↓↓↓\n' + bab_select[1] + '\n★★★★★★★★★★★★★'

    return bab_response

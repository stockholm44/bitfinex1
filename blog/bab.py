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
    elif data == '파주 P8공장뒤':
        bab_list = {'기린(짱깨)': 'http://naver.me/FfpYq6GQ',
                    '신돼야지 두루치기':'http://naver.me/xNv2h4Je',
                    '한양짬뽕 파주LCD점':'http://naver.me/Gd3ujXKK',
                    '닐리 LCD산업단지점':'http://naver.me/F5erJhzc',
                    '옛날전통육개장(육대장(?))':'http://naver.me/xwbsOPwQ',
                    '전계능식당 파주LCD점 ':'http://naver.me/GoaXtNkI'}
    elif data == '파주 LGD기숙사뒤':
        bab_list = {'깜쪽':'http://naver.me/GNj6goyh',
                    '대판 숯불구이':'http://naver.me/5oI4YOVU',
                    '맘보집파주LCD점':'http://naver.me/xrgMNx4G',
                    '육갑':'http://naver.me/5zCsb3KK',
                    '고기의 품격':'http://naver.me/Gu9jgrMX',
                    '만우가든':'http://naver.me/GJbgP3FV',
                    '숯껌뎅이':'http://naver.me/F0MWH861',
                    '용용횟집':'http://naver.me/5KhH4ZnY',
                    '백년불보쌈불족발 월롱엘지점':'http://naver.me/FCNf6XnW',
                    '토평한우소곱창':'http://naver.me/Gu9jgGcw',
                    '초원':'http://naver.me/GEfvb5ng',
                    '신의주찹쌀순대 파주LG디스플레이점':'http://naver.me/F2tbfYKo'}
    elif data == '파주 내 그외지역':
        bab_list = {'갈릴리농원': 'http://naver.me/FRdn4vAf',
                    '파주닭국수 파주본점':'http://naver.me/51c0FiF9',
                    '신간짬뽕':'http://naver.me/FYpzdeOO',
                    '문산삼거리부대찌개':'http://naver.me/GoaBccOu',
                    '정미식당 부대찌개':'http://naver.me/xNv2haNA',
                    '밀밭식당':'http://naver.me/59Eq9SBB',
                    '남기남부대찌개':'http://naver.me/GGVP618D',
                    '참두루 두루치기':'http://naver.me/5azHLmHC'}

    bab_place = ['화정','일산','관산동','연희동','홍대','파주 P8공장뒤','파주 LGD기숙사뒤','파주 내 그외지역']
    bab_select = random.choice(list(bab_list.items()))
    bab_response = data + ' 지역에서 고를수 있는 \n♥랜덤맛집♥ 은 다음과 같습니다.\n★★★★★★★★★★★★★\n\n 맛집이름 : ' + str(bab_select[0]) + '\n\n네이버 지도 링크 ↓↓↓↓\n' + str(bab_select[1]) + '\n\n★★★★★★★★★★★★★'

    return bab_response, bab_place

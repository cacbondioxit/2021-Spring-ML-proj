# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs

with open('temptemp1.html', mode='r', encoding='utf-8') as fp:

    a = ''.join([x for x in fp.readlines()])
    aa= bs(a, 'lxml')

    b1= aa.find("div", {"class" : "product-list-body"})
    b2= b1.find_all_next("div", {"class" : "product-card"})

    for x in b2:
        # 건물 종류
        print(x.find("div", {"class" : "court-txt"}).contents[0].strip())

        # 사건 번호
        print(x.find("span", {"class" : "address-txt address-number"}).contents[0].strip())

        addr_size = x.find("a", {"class" : "detail-popup"})
        # 경매 물건 주소
        addr = addr_size.find("span", {"class" : "address-txt"}).contents[0].strip()
        # 경매 물건 크기
        size = addr_size.find("div", {"class" : "size-txt"}).contents[0].strip()
        print(f"{addr=}")
        print(f'{size=}')

        # 가격
        prices =x.find("div", {"class" : "label-price-group"})

        # 감정가
        t1 =prices.find("div", {"class" : "label-appraiser-price"})
        print(t1.find("div", {"class" : "price-value"}).contents[0].strip())

        # 최저가
        t2 = prices.find("div", {"class" : "label-lowest-price"})
        if t2 :
            print(t2.find("div", {"class" : "price-value"}).contents[0].strip())

        # 낙찰가
        t3 = x.find("div", {"class" : "label-winning-price"})
        if t3:
            print(t3.find("div", {"class" : "price-value"}).contents[0].strip())

        print('-=' * 5)
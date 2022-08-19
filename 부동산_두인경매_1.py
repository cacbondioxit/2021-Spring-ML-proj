# -*- coding: utf-8 -*-

import csv
from dataclasses import dataclass
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import random
import re


CASE_YEAR = 2015
RECORD_PER_PAGE = 100

@dataclass
class KMCourts:
    서울 = ['101','102','103','104','105']
    의정부 = ['106', '107']
    수원 = ['301','302','303','304','305', '306']
    인천 = ['201', '202']
    대구 = ['701', '702','703','704','705','706','707','708', '709']
    울산 =['D01']
    창원 =['B01','B02','B03','B04','B05','B06']
    부산 =['601','602','603']
    춘천 =['501','502','503','504','505']
    청주 =['A01','A02','A03','A04']
    대전 =['401','402','403','404','405','406']
    전주 =['C01','C03','C02','C04']
    광주 =['801','802','803','804','805']
    제주 =['901']

    startURL : str = "court1%5B%5D="    # court1[]=
    sep : str = "%7C" # |

@dataclass
class KMStatus:
    all : str = "all"
    진행 : str = "ing"
    매각전부 : str = "낙찰%7C허가%7C대납%7C배당%7C종결"

    start : str = "km_status="

@dataclass
class KMType:
    주거용  = ['121', '124','111','131', '112']
    상업용  = ['222','211','224','223','433','435','311','321','41F','456','411','421','412','215','416','418','413','2ZZ']
    sep : str = 'mul_type%5B%5D='

@dataclass
class SearchURLBuild:
    current_page : int = 1
    records_per_page : int = 30

def makeURL(pagenum : int, year : int):
    '''
    귀찮아서 일단 
        서울 법원 전체
        주거용
        경매현황 전체
    이렇게 가져옴 
    '''
    searchURLbase = "https://www.dooinauction.com/auction/search/?"

    km_court = KMCourts()
    km_status = KMStatus()
    km_type = KMType()

    url = str(searchURLbase)

    url += km_court.startURL + km_court.sep.join(km_court.서울)
    url += '&'


    url += "case_number_year="
    url += str(year)
    url += '&'

    url += km_status.start + km_status.all
    url += '&'

    aa  = [km_type.sep + x for x in km_type.상업용 ]
    url += '&'.join(aa)
    url += '&'

    # &current_page=1&records_per_page=100

    url += f'current_page={pagenum}'
    url += '&'

    url += f'records_per_page={RECORD_PER_PAGE}'

    return url 

@dataclass
class Records:
    build_type : str
    case_num : str
    addr : str
    size : str
    appraiser : str
    lowest : str
    success : str
    start_date : str

    def toCSV(self, ):
        return [
            self.build_type,
            self.case_num,
            self.addr,
            self.size,
            self.appraiser,
            self.lowest,
            self.success,
            self.start_date
        ]

def crawlData(year):
    items = []
    rrr = []

    options = webdriver.ChromeOptions()
    # options.add_argument('headless') # headless로 하면 웹 브라우저 html linting 기능이 동작하지 않아, JS로 불러온 html이 정렬되지 않아 파싱이 불가능해짐
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)


    ffp = open(f'save-공업용-{year}.csv', mode='w',newline='', encoding='utf-8')
    CSVWritter = csv.writer(ffp)

    pg = 1
    while True:
        urlll = makeURL(pg, year)
        driver.get(urlll)
        driver.set_page_load_timeout(3)
        
        time.sleep(2) # 바로 닫으면 linting이 안됨 --> 잠시 대기

        aa = bs(driver.page_source, 'lxml')
        
        bb= aa.find("div", {"class" : "product-list-body"})

        if not len(bb.find_all("div",{"class" : "product-card"})):
            break
        
        for item in bb.find_all("div",{"class" : "product-card"}):
            # try:
            # 건물 종류
            if popop := item.find("div", {"class" : "court-txt"}):
                build_type = popop.contents[0].strip()
            else:
                build_type = ''

            # 사건 번호
            if ttkt := item.find("span", {"class" : "address-txt address-number"}):
                case_num = ttkt.contents[0].strip()
            else:
                case_num = ''

            addr_size = item.find("a", {"class" : "detail-popup"})

            # 경매 물건 주소
            if addr_size:
                if kkk := addr_size.find("span", {"class" : "address-txt"}):
                    addr = kkk.contents[0].strip()
                    # re.findall(".*(외.*개 목록)$", addr)
                    searches = re.search(".*( 외 [0-9]+개).*$", addr)
                    remove_area = None

                    if searches:
                        if len(searches.regs[1:]) > 1:
                            s, e = searches.regs[1][0], searches.regs[-1][1]
                        else:
                            s, e  = searches.regs[1]
                        addr = addr[ :s]
                else:
                    addr =''
                # 경매 물건 크기
                if tttt := addr_size.find("div", {"class" : "size-txt"}):
                    size = tttt.contents[0].strip()
                else:
                    size =''
            else:
                addr =''
                size =''

            # 가격
            if lllll := item.find("div", {"class" : "label-price-group"}):
                prices = lllll

            if prices:
                # 감정가
                if t1:= prices.find("div", {"class" : "label-appraiser-price"}):
                    appraiser = t1.find("div", {"class" : "price-value"}).contents[0].strip()

                # 최저가
                t2 = prices.find("div", {"class" : "label-lowest-price"})
                if t2 :
                    lowest = t2.find("div", {"class" : "price-value"}).contents[0].strip()
                else:
                    lowest = ''

                # 낙찰가
                t3 = prices.find("div", {"class" : "label-winning-price"})
                if t3:
                    success = t3.find("div", {"class" : "price-value"}).contents[0].strip()
                else:
                    success=''
            else:
                appraiser =''
                lowest =''
                success =''

            t4 = item.find("div", {"class" : "product-card-cell product-card-date"})
            if t4 and (asdqwd := t4.find("div", {"class" : "date-day"})):
                start_date = asdqwd.contents[0].strip()
            else:
                # 취하 일 경우 날짜 없음
                start_date =''
            # except Exception as a:
            #     print(a)
            #     print(f'{urlll=}')

            record = Records(build_type,case_num,addr,size,appraiser,lowest,success,start_date)
            rrr.append(record)

        with open(f'./htmls/{year}-{pg}-{RECORD_PER_PAGE}.html', mode='w', encoding='utf-8') as fp:
            fp.write(aa.prettify(formatter='html'))

        sleeping = 4 + random.random()*3
        print(f'페이지 {pg} 완성!, sleeping... {sleeping:.5f} 초')

        time.sleep(sleeping)
    
        pg += 1

    CSVWritter.writerow(['building type', 'case num', 'address', 'size', 'appraiser', 'lowest', 'success', 'bid_date'])
    
    for x in rrr:
        CSVWritter.writerow(x.toCSV())

    driver.close()

# for x in [2015, 2016, 2017, 2018, 2019, 2020]:
for x in [2010, 2011, 2012, 2013, 2014]:
    crawlData(x)
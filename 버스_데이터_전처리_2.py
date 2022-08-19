year = [2015, 2016, 2017, 2018]
month= ['01', '02', '03','04','05','06','07','08','09','10','11','12']

head2 = ['사용일자', '버스정류장ARS번호', '역명', '승차총승객수', '하차총승객수', 'CRDNT_Y', 'CRDNT_X']

head2 = ['사용일자', '주차', '버스정류장ARS번호', '역명', '승차총승객수', '하차총승객수', 'CRDNT_Y', 'CRDNT_X']

head4 = ['주차', '버스정류장ARS번호', '역명', '승차총승객수', '하차총승객수', 'CRDNT_Y', 'CRDNT_X', '주말']

'''
버스 정류장 별로 주차마다 승하차객 숫자 정보임
정류장 개수가 (없어진 정류장 제외해도) 몇 천개다보니 주차마다 나눠서 보는 것이 유용할 것 같음
'''
from datetime import datetime
# 월 ~ 일요일 기준으로 주(week) 계산 YEAR / Week Num / 1~7 (월~일)
# print(datetime(2022, 5, 9).isocalendar())ㄴ

import os, pathlib, csv


def main(y):
    data = []

    tofile = f"weekNum/BUS_filte_{y}.csv"

    save_to = pathlib.WindowsPath(os.getcwd(), tofile)

    ddir = os.path.dirname(save_to)
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    # key : (주차, 정류소 이름) : (승차 , 하차)
    busstations = {}
    for m in month:
        print(f'starting MONTH : {m}')
        fromfile = f"changed/{y}/BUS_filte_{y}_{m}.csv"
        with open(f'{fromfile}', mode='r', encoding='utf-8') as fp:
            csvreader = csv.reader(fp)
            headers = next(csvreader)

            for line in csvreader:
                date_ = line[0]
                yyyy, mm, dd = int(date_[0:4]), int(date_[4:5+1]), int(date_[6:7+1])
                # print(yyyy, mm, dd )

                weeknum = datetime(yyyy, mm, dd).isocalendar()[1]
                # print(datetime(yyyy, mm, dd), datetime(yyyy, mm, dd).isocalendar()[1])

                line.insert(1, weeknum)

                if val := busstations.get((line[1], line[2]), None):
                    up, down = val
                    busstations[(line[1], line[2])] = (up+int(line[4]), down + int(line[5]))
                else:
                    busstations[(line[1], line[2])] = (int(line[4]), int(line[5]))
                    data.append(line)
            
            for dat in data:
                up_, down_ = busstations[(dat[1], dat[2])]
                dat[4], dat[5] = up_, down_

    with open(f'{tofile}', mode='a+', encoding='utf-8', newline='') as fp:
        csvwriter = csv.writer(fp)
        csvwriter.writerow(head2)
        csvwriter.writerows(data)

'''
이거는 평일, 주말
'''
def main2(y):
    data = []

    tofile = f"weekend/BUS_filte_{y}.csv"
    save_to = pathlib.WindowsPath(os.getcwd(), tofile)

    ddir = os.path.dirname(save_to)
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    # key : (주차, 정류소 이름) : (승차 , 하차)
    busstations = {}

    for m in month:
        print(f'starting MONTH : {m}')
        fromfile = f"changed/{y}/BUS_filte_{y}_{m}.csv"
        with open(f'{fromfile}', mode='r', encoding='utf-8') as fp:
            csvreader = csv.reader(fp)
            headers = next(csvreader)

            for line in csvreader:
                date_ = line[0]
                yyyy, mm, dd = int(date_[0:4]), int(date_[4:5+1]), int(date_[6:7+1])
                # print(yyyy, mm, dd )

                weeknum = datetime(yyyy, mm, dd).isocalendar()[1]
                weekend = datetime(yyyy, mm, dd).weekday() > 4 # 주말
                # print(datetime(yyyy, mm, dd), datetime(yyyy, mm, dd).isocalendar()[1])

                line.insert(1, weeknum)
                line.append(weekend)

                if val := busstations.get((line[1], line[2], line[-1]), None):
                    up, down = val
                    busstations[(line[1], line[2],  line[-1])] = (up+int(line[4]), down + int(line[5]))
                else:
                    busstations[(line[1], line[2],  line[-1])] = (int(line[4]), int(line[5]))
                    data.append(line[1:])
            
            for dat in data:
                up_, down_ = busstations[(dat[0], dat[1],  dat[-1])]
                dat[3], dat[4] = up_, down_

    with open(f'{tofile}', mode='a+', encoding='utf-8', newline='') as fp:
        csvwriter = csv.writer(fp)
        if m=='01':
            csvwriter.writerow(head4)
        csvwriter.writerows(data)

if __name__ == '__main__':
    # for y in year:
    #     print(f'starting YEAR : {y}')
    #     main(y)

    for y in year:
        print(f'starting YEAR : {y}')
        main2(y)
            
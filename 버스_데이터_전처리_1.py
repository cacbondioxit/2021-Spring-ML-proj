
YEAR = 2015
MONTH = "03"

import csv
from dataclasses import dataclass
import pathlib


head = ['사용일자', '노선번호', '노선명', '버스정류장ARS번호', '역명', '승차총승객수', '하차총승객수', '등록일자']
head2 = ['사용일자', '버스정류장ARS번호', '역명', '승차총승객수', '하차총승객수', 'CRDNT_Y', 'CRDNT_X']

haedspace = [ x in head2 for x in head]

@dataclass
class BUS:
    node_id : str
    station_name : str
    id_ : str
    cord_x : str
    cord_y : str

bus_coord = dict()

year = [2015, 2016, 2017, 2018]
month= ['01', '02', '03','04','05','06','07','08','09','10','11','12']

import os
def main(year, month):

    bus_stations = dict()
    data = []
    bus = f"BUS_STATION_BOARDING_MONTH_{year}{month}.csv"
    save_to = f"changed/{year}/BUS_filte_{year}_{month}.csv"
    
    save_to = pathlib.WindowsPath(os.getcwd(), save_to)

    ddir = os.path.dirname(save_to)
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    # 버스 좌표 있는 곳
    with open('bus-data-2019.csv', mode='r', encoding='utf-8') as fp:
        csvreader = csv.reader(fp)
        next(csvreader)
        # NODE_ID(노드ID),STTN_NM(정류소명칭),STTN_NO(정류소ID),CRDNT_X(X좌표),CRDNT_Y(Y좌표)
        for _, _, id, x, y in csvreader:
            # print(id, x, y)
            bus_coord[int(id)] = (x, y)
    # 버스 
    with open(f'./{year}/{bus}', mode='r', encoding='cp949') as fp:
        csvreader = csv.reader(fp)

        headers = next(csvreader)
        for line in csvreader:
            a = [it if Bool else None for it, Bool in zip(line, haedspace)]

            # 현재 존재하지 않는 정류장의 경우
            if a[3] == '~':
                continue

            need = [a[0], *a[3:7]]
            # print(f"{need=}")
            data.append(need)

    data2 = []
    for dat in data:
        if coord := bus_coord.get(int(dat[1]), None):
            dat += list(coord)[::-1]
            # CRDNT_X(X좌표),CRDNT_Y(Y좌표) -> CRDNT_Y(Y좌표), CRDNT_X(X좌표) 이렇게 바꿈 
            data2.append(dat)
        else:
            assert f"{dat=} | {coord=}"

    '''
    같은 날짜에 중복된 데이터가 있음, 하루에 정류장 10명은 말이 안되는 것 같고
    분할되어서 저장된 것 같다

    분할되어서 저장된게 맞고
    100만개 정도 있었던(1달 데이터) 데이터를 취합해서 하루 날짜별 승하차를 합쳐보니 30만개로 줄었다.

    대략 정류장은 9천개 중반 정도 되는듯
    '''
    for dat in data2:
        yymmdd, station_id, name, up, down, y, x  = dat

        if nya := bus_stations.get((yymmdd, station_id, name), None):
            bus_stations[(yymmdd, station_id, name)] = [yymmdd, station_id, name, int(nya[3]) + int(up), int(nya[4]) + int(down), y, x]
        else:
            bus_stations[(yymmdd, station_id, name)] = dat

    aa = sorted([v for k, v in bus_stations.items()], key=lambda x : x[0])
    
    with open(save_to, newline='', mode='w', encoding='utf-8') as fp:
        csvwritter = csv.writer(fp)
        csvwritter.writerow(head2)
        csvwritter.writerows(aa)

for y in year:
    print(f'doing YEAR :{y} ')
    for m in month:
        print(f'doing MONTH :{m}')
        main(y, m)
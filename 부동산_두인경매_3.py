from datetime import datetime
# 월 ~ 일요일 기준으로 주(week) 계산 YEAR / Week Num / 1~7 (월~일)
# print(datetime(2022, 5, 9).isocalendar())ㄴ

import os, pathlib, csv


aa = "save-공업용-{}.csv"

bb  = ['building type','case num','address','size','appraiser','lowest','success','bid_date']

cc = "낙찰-공업용-{}.csv"

savedFor = dict()


def main(year):

    data = []
    data.append(bb)

    with open(aa.format(year), mode='r', encoding='utf-8') as fp:

        csvreader = csv.reader(fp)

        next(csvreader)

        for x in csvreader:
            if x[-1]:
                yyyy, mm, dd = map(lambda x : int(x),  x[-1].split('-'))
                da = datetime(yyyy, mm, dd)
                if da.year == year:
                    data.append(x)

                else:
                    if savedFor.get(da.year, None):
                        savedFor[da.year].append(x)
                    else:
                        savedFor[da.year] = [x]

    if year>=2015:
        with open(cc.format(year), mode='w',newline='' ,encoding='utf-8') as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerows(data)

            if tt := savedFor.get(year, None):
                csvwriter.writerows(tt)

for x in  range(2010, 2017+1):
    main(x)
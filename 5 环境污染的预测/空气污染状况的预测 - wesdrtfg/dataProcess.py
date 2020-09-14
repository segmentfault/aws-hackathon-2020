import os
from types import *
from typing import *
import re
import json


data: Dict[str, Any] = dict()

for fn in os.listdir("beijingAir"):
    f = open('beijingAir/' + fn, encoding='utf8')
    #f = open('beijingAir/beijing_all_20140503.csv', encoding='utf8')
    day: Dict[str, List[Tuple[str, float]]] = dict()
    for d in f.readlines()[1:]:
        row = d.split(',')
        if len(row) < 4 or row[2].find('h') != -1:
            continue
        time = row[0] + row[1]
        num = 0.0
        try:
            num = float(row[3])
        except:
            continue
        if time not in day:
            day[time] = list()
        day[time].append((row[2], num))
    
    for time in day:
        d = dict()
        d['time'] = time
        for i in day[time]:
            d[i[0]] = i[1]
        data[time] = d


for d in os.listdir('global/'):
    for dd in os.listdir('global/' + d):
        for fn in os.listdir('global/' + d + '/' + dd):    
            if fn.find('545110') == -1:
                continue
            f = open('global/' + d + '/' + dd +  '/' + fn)
            rows = f.readlines()
            for r in rows:
                col = re.split('\s+', r)
                if len(col) < 9:
                    continue
                if col[4] == '-9999' or col[5] == '-9999' or col[7] == '-9999' or col[8] == '-9999':
                    continue
                time = col[0] + col[1] + col[2] + col[3]
                if time not in data:
                    continue
                Atemp: float
                Dtemp: float
                windA: float
                windR: float
                try:
                    Atemp = float(col[4])
                    Dtemp = float(col[5])
                    windA = float(col[7])
                    windR = float(col[8])
                except:
                    continue
                data[time]['Atemp'] = Atemp / 10.0
                data[time]['Dtemp'] = Dtemp / 10.0
                data[time]['windA'] = windA / 10.0
                data[time]['windR'] = windR / 10.0

delLst = []
for k in data:
    if len(data[k]) != 8:
        delLst.append(k)

for i in delLst:
    data.pop(i)

data = json.dumps(data)
ff = open('data.json', 'w')
ff.write(data)
ff.close()
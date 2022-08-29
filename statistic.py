#this module should monitor the usage of my bot
from datetime import date
import json

def jsonRead():
    with open('quantityStat.json') as f:
        info = json.load(f)
    return info

def jsonWrite(info):
    with open('quantityStat.json', 'w') as f:
        f.write(json.dumps(info))

def quantity():
    pass

def getUserList():
    pass

def getQuantity():
    pass

print(date.today())

def counter():
    todayDate = str(date.today())
    info = jsonRead()
    if todayDate in info:
        info[todayDate] += 1
    else:
        info[todayDate] = 1
    jsonWrite(info)
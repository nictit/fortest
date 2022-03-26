#for future make ship as an class with objects of ships
from requests import get
from bs4 import BeautifulSoup
import shipsList

#required initializing parameters
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
token = '5048232576:AAHKQXWuVI-KIFQOEsDEizTGo9A1Ahjk4cw'

# read ships.csv file and make tuples with norway and canadian ships
# each of them contain 3 parameters: country, c/s, mmsi
def fileReader():
    nor_ships, cdn_ships = shipsList.ships()
    return nor_ships, cdn_ships

#input - mmsi code from tuples nor_ship and cdn_ship
#output - html code of the ship page with info about its c/s,
#position etc
def getPageSource(mmsi):
    url = 'https://www.vesselfinder.com/vessels?name=' + str(mmsi)
    response = get(url, headers=HEADERS, timeout=None)
    soup = BeautifulSoup(response.content, features='lxml')
    address = soup.find('a', attrs={'class': 'ship-link'})
    url = 'https://www.vesselfinder.com' + address['href']
    response = get(url, headers=HEADERS, timeout=None)
    return BeautifulSoup(response.content, features='lxml')

# get c/s, position, time from source in minutes
def getInfo(page_source):
    ship_location = page_source.find('p', attrs={'class':'text2'}).text
    first_coordinate = ship_location[ship_location.find('coordinates') + len('coordinates') + 1:ship_location.find('/', ship_location.find('coordinates'))-1]
    second_coordinate = ship_location[ship_location.find('/',ship_location.find('coordinates')) + 1:ship_location.find(')', ship_location.find('coordinates'))]
    ship_callsign_and_time = page_source.find('table', attrs={'class': 'aparams'}).text
    callsign = ship_callsign_and_time[ship_callsign_and_time.find('Callsign') + len('Callsign'):ship_callsign_and_time.find('Callsign') + len('Callsign') + 4]
    if not (callsign.isalpha() and callsign.isupper() and len(callsign)==4):
        callsign = 'error'
    time = ship_callsign_and_time[ship_callsign_and_time.find('Position received') + len('Position received') + 1:ship_callsign_and_time.find('ago') + 3]
    time = timeconventer(time)
    first_coordinate,  second_coordinate = decToDegree(first_coordinate,second_coordinate)
    ship_info = [callsign, first_coordinate, second_coordinate, time]
    return ship_info

def timeconventer(time: str):
    if 'min' in time:
        time = str([int(s) for s in time.split() if s.isdigit()][0])
        return (time)
    elif 'hour' in time:
        time = str([int(s) for s in time.split() if s.isdigit()][0])
        return (str(int(time) * 60))
    elif 'day' in time:
        time = str([int(s) for s in time.split() if s.isdigit()][0])
        return (str(int(time) * 1440))

# conversion of coordinates
def decToDegree(first_coordinate_dec,second_coordinate_dec):
    minutes1, sec1 = divmod(float(first_coordinate_dec[:-2]) * 3600, 60)
    deg1, minutes1 = divmod(minutes1, 60)
    minutes2, sec2 = divmod(float(second_coordinate_dec[:-2]) * 3600, 60)
    deg2, minutes2 = divmod(minutes2, 60)
    first_coordinate_degree = str(round(deg1)) + u"\u00b0" + str(round(minutes1)) + "'" + str(round(sec1)) + '"' + first_coordinate_dec[-2:]
    second_coordinate_degree = str(round(deg2)) + u"\u00b0" + str(round(minutes2)) + "'" + str(round(sec2)) + '"' + second_coordinate_dec[-2:]
    return first_coordinate_degree, second_coordinate_degree

def output(ship):
    ship[3] = int(ship[3])
    if ship[3] >= 1440:
        ship[3] = round(ship[3] / 1440)
        out = ship[0] + ': ' + ship[1] + ' ' + ship[2] + ' (' + str(ship[3]) + ' days ago)'
    elif ship[3] > 60:
        ship[3] = round(ship[3] / 60)
        out = ship[0] + ': ' + ship[1] + ' ' + ship[2] + ' (' + str(ship[3]) + ' hr ago)'
    else:
        out = ship[0] + ': ' + ship[1] + ' ' + ship[2] + ' (' + str(ship[3]) + ' min ago)'
    return out


def main():
    nor_ships, cdn_ships = fileReader()
    
    nor_ships_info = []
    cdn_ships_info = []

# add time filter: if last ship position recieved > 15 hr *60 = 900 min ago then delete it
    for ship in nor_ships:
        nor_ships_info.append(getInfo(getPageSource(ship[2])))
        print('1')
    nor_ships_info = sorted(nor_ships_info, key= lambda x: int(x[3]))
    for ship in cdn_ships:
        cdn_ships_info.append(getInfo(getPageSource(ship[2])))
        print('2')
    cdn_ships_info = sorted(cdn_ships_info, key= lambda x: int(x[3]))

    nor = ''
    cdn = ''
    for ship in nor_ships_info[:3]:
        nor += output(ship)
        nor += '\n'
    for ship in cdn_ships_info[:3]:
        cdn += output(ship)
        cdn += '\n'
    allShipsMsg = nor + '\n' + cdn
    return allShipsMsg

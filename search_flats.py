import requests
from bs4 import BeautifulSoup

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

places = ['Warszawa','Krakow', 'Lodz', 'Wroclaw', 'Poznan', 'Gdansk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Bialystok']
offers = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
db = SQLAlchemy(app)

class Flats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    '''add'''
    # address = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    '''new add'''
    link = db.Column(db.String)



db.create_all()


def parse_price(price):
    return price.replace(' ', '').replace('zł', '')


def page(number, i):
    URL = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie'
    response = requests.get(f'{URL}/{i}?page={number}')
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def parse_link(link):
    response = requests.get(link)
    content = response.text
    soup = BeautifulSoup(content,'html.parser')
    return soup

def parse_page(number:int, places:str) -> None:
    for place in places:
        print(f'Number {number}')
        soup = page(number, place)
        for offer in soup.find_all('li', class_='css-p74l73'):
            try:
                link = offer.find('a', class_='css-rvjxyq')['href']
            except NameError:
                link = None
            else:
                try:
                    link = f'https://www.otodom.pl/{link}'
                    new = parse_link(link)
                    information = new.find_all('a', class_='css-1in5nid')
                    info = [info.getText() for info in information]
                    # print(info)
                    city = info[2]
                    province = info[1]
                    district = info[3]

                    try:
                        settlement = info[4]
                    except IndexError:
                        settlement = None

                    try:
                        street = info[5]
                    except IndexError:
                        street = None

                    price = new.find('strong', class_='css-8qi9av').getText().replace(' ', '').split('zł')[0]
                    info_2 = new.find_all('div', class_='css-1wi2w6s')
                    details = [info.getText() for info in info_2]
                    area = details[0].split(' ')[0]
                    own = details[1]
                    rooms = details[2]
                    finishing = details[3]
                    try:
                        level = details[4]
                    except IndexError:
                        level = None
                    else:
                        level.split('/')
                        print(level)
                        if level[0] == 'parter':
                            level[0] = 0
                            level = f'{level[0]}/{level[1]}'

                    try:
                        rent = details[6].split(' ')[0]
                    except IndexError:
                        rent = None
                    try:
                        parking = details[7]
                        print(parking)
                    except KeyError:
                        parking = None

                    try:
                        heating = details[9]
                    except KeyError:
                        heating = None
                except IndexError:
                    break
            print(
                f'city: {city} - price : {price} - area: {area} - rooms: {rooms}- {link} - finishing: {finishing} - level: {level} - rent:{rent} - parking: {parking} - heating:{heating} - own: {own}- province: {province} - district"{district} - settlement: {settlement} - street:{street}')






            # link = ''
            '''Do poprawy, nie dodajemy do bazy danych po wierszu, tylko dodac wszystkie wiersze i dopiero wtedy commit'''
            new_flat = Flats(
                city=city,
                price=price,
                area=area,
                room=rooms,
                link=link
            )
            # offers.append(new_flat)

            db.session.add(new_flat)
            db.session.commit()
            print(f'{city} - {area} - {price} - {rooms}')

# db.session.add(offers)
# db.session.commit()

for i in range(1,2):
    parse_page(i, places)












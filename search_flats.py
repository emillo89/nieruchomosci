import requests
from bs4 import BeautifulSoup

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

places = ['Warszawa','Krakow', 'Lodz', 'Wroclaw', 'Poznan', 'Gdansk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Bialystok']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
db = SQLAlchemy(app)

class Flats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    room = db.Column(db.Integer, nullable=False)


db.create_all()


def parse_price(price):
    return price.replace(' ', '').replace('zł', '')


def page(number, i):
    URL = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie'
    resonse = requests.get(f'{URL}/{i}?page={number}')
    content = resonse.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def parse_page(number:int, places:str) -> None:
    for place in places:
        print(f'Number {number}')
        soup = page(number, place)
        for offer in soup.find_all('li', class_='css-p74l73'):
            city = offer.find('span', class_='css-17o293g').getText().split(',')[0]
            try:
                area = offer.find('div', class_='css-i38lnz').getText()
            except IndexError:
                area = offer.find('div', class_='css-i38lnz').getText()
            else:
                if 'pokój' in area:
                    area = area.replace('pokój', 'pokoje')
                elif 'pokoi' in area:
                    area = area.replace('pokoi', 'pokoje')
                area = area.split('pokoje')[1].split(' ')[0]

            price = parse_price(offer.find('span', class_='css-rmqm02').getText())
            rooms = offer.find('div', class_='css-i38lnz').getText().split('m²')[1].split(' ')[0]


            # link = ''
            '''Do poprawy, nie dodajemy do bazy danych po wierszu, tylko dodac wszystkie wiersze i dopiero wtedy commit'''
            new_flat = Flats(
                city = city,
                price = price,
                area = area,
                room = rooms
            )
            db.session.add(new_flat)
            db.session.commit()

            print(f'{city} - {area} - {price} - {rooms}')


for i in range(1,2):
    parse_page(i, places)












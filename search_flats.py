from datetime import datetime,date
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webscrapping import parse_price,change_zapytaj,check_price,page,parse_link



places = ['Warszawa','Krakow', 'Lodz', 'Wroclaw', 'Poznan', 'Gdansk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Bialystok']
offers = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
db = SQLAlchemy(app)


class Flats(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    rooms = db.Column(db.Integer,nullable=True)
    link = db.Column(db.String(256), nullable=True)
    own = db.Column(db.String(100), nullable=True)
    finishing = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(10), nullable=True)
    rent = db.Column(db.Integer, nullable=True)
    parking = db.Column(db.String(100), nullable=True)
    heating = db.Column(db.String(100), nullable=True)
    market = db.Column(db.String(100), nullable=True)
    advertisement = db.Column(db.String(100), nullable=True)
    # years_of_building = db.Column(db.DateTime, nullable=True)
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    settlement = db.Column(db.String(100))
    street = db.Column(db.String(100))
    date_add_to_date = db.Column(db.DateTime, default=datetime.utcnow)



db.create_all()


def create_new_flat(city, price, area, rooms, link, own, finishing, level, rent, parking, heating, market,
                    advertisement, years_of_building, province, district, settlement, street, date_add_to_date):

    new_flat = Flats(
        city=city,
        price=price,
        area=area,
        rooms=rooms,
        link=link,
        own=own,
        finishing=finishing,
        level=level,
        rent=rent,
        parking=parking,
        heating=heating,
        market=market,
        advertisement=advertisement,
        # years_of_building=years_of_building,
        province=province,
        district=district,
        settlement=settlement,
        street=street,
        date_add_to_date=date_add_to_date
    )
    offers.append(new_flat)


def parse_page(number:int, places:str) -> None:
    for place in places:
        print(f'Number {number}')
        soup = page(number, place)
        for offer in soup.find_all('li', class_='css-p74l73'):
            print(offer)
            link = offer.find('a', class_='css-rvjxyq')['href']

            try:
                link = f'https://www.otodom.pl/{link}'
                new = parse_link(link)

                information = new.find_all('a', class_='css-1in5nid')
                info = [info.getText() for info in information]
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

                if check_price(price) == True:
                    break


                info_2 = new.find_all('div' , class_='css-1qzszy5')
                details = [info.getText() for info in info_2]

                area = change_zapytaj(details[1].split(' ')[0]).replace(',','.')
                own = change_zapytaj(details[3])
                rooms = change_zapytaj(details[5])
                finishing = change_zapytaj(details[7])
                level = change_zapytaj(details[9].split('/'))
                if level[0] == 'parter':
                    level[0] = 0
                level = f'{level[0]}/{level[1]}'
                rent = change_zapytaj(details[13].replace(' ','').split('zł')[0])
                parking = change_zapytaj(details[15])
                heating = change_zapytaj(details[19])
                market = change_zapytaj(details[21])
                advertisement = change_zapytaj(details[23])
                years_of_building = change_zapytaj(details[25])

                # if years_of_building in ['blok', 'apartamentowiec','plastikowe', 'kamienica']:
                #     years_of_building = None

                # nr_offers = new.find('div', class_='css-jjerc6').getText()
                # data_off_addition = new.find('div', class_='css-atkgr').getText()
                date_add_to_date = date.today()

            except IndexError:
                break

            else:
                create_new_flat(city, price, area, rooms, link, own, finishing, level, rent, parking, heating, market,
                                advertisement, years_of_building,province, district, settlement, street, date_add_to_date)

                # print(f'{date_add_to_date} - {years_of_building} ')


                print(f'city: {city} - price : {price} - area: {area} - rooms: {rooms}- link: {link} - finishing: {finishing} - level: {level} - rent:{rent} - parking: {parking} -market: {market} - advertisement:{advertisement} -years_of_building: {years_of_building}-  heating:{heating} - own: {own}- province: {province} - district{district} - settlement: {settlement} - street:{street}')

for i in range(1):
    parse_page(i, places)
#
# db.session.add_all(offers)
# db.session.commit()











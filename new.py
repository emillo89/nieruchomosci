import json
import re
import time
from datetime import datetime,date
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from sqlalchemy.orm import Session

places = ['Warszawa','Krakow', 'Lodz', 'Wroclaw', 'Poznan', 'Gdansk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Bialystok']
offers = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
db = SQLAlchemy(app)


class Flats(db.Model):
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
    # date_add_to_date = db.Column(db.DateTime, default=datetime.utcnow)



db.create_all()


def parse_price(price):
    return price.replace(' ', '').replace('zł', '')


def page(number, i):
    URL = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie'
    resonse = requests.get(f'{URL}/{i}?page={number}')
    content = resonse.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def parse_link(link):
    response = requests.get(link)
    content = response.text
    soup = BeautifulSoup(content,'html.parser')
    return soup


def change_zapytaj(text):
    if text == 'zapytaj':
        text = None
    return text


def check_price(text):
    if text == 'Zapytajocenę':
        return True
    return False


def create_new_flat(city, price, area, rooms, link, own, finishing,level, rent, parking, heating, market,
                    advertisement, province, district, settlement,street):
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
        # date_add_to_data=date_add_to_data
    )
    offers.append(new_flat)


def parse_page(number:int, places:str) -> None:
    for place in places:
        print(f'Number {number}')
        soup = page(number, place)
        for offer in soup.find_all('li', class_='css-p74l73'):
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
                if years_of_building in ['blok', 'apartamentowiec']:
                    years_of_building = None

                date_add_to_data = date.today()

            except IndexError:
                break

            else:
                create_new_flat(city, price, area, rooms, link, own, finishing, level, rent, parking, heating, market,
                                advertisement, province, district, settlement, street)

                print(offers)


            # print(f'city: {city} - price : {price} - area: {area} - rooms: {rooms}- link: {link} - finishing: {finishing} - level: {level} - rent:{rent} - parking: {parking} -market: {market} - advertisement:{advertisement} -years_of_building: {years_of_building}-  heating:{heating} - own: {own}- province: {province} - district{district} - settlement: {settlement} - street:{street}')

# for i in range(1):
#     parse_page(i, places)
# db.session.add_all(offers)
# db.session.commit()

# for place in offers:
#     db.session.add(place)
# db.session.commit()

# import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import sqlite3
connection = sqlite3.connect('flats.db')
df = pd.read_sql_query("Select * from property", connection)
print(df.columns)

to_csv = df.to_csv('flats.csv')

# sq1 = """ SELECT * FROM property"""
# df = pd.read_sql_query(sq1, con)
# print(df)
# URL = 'https://www.otodom.pl/pl/oferta/penthouse-z-tarasem-ponad-80m2-na-dachu-ID4h88X'
# response = requests.get(URL)
# content = response.text
# soup = BeautifulSoup(content, 'html.parser')
# scrapt_tag = soup.find("script", scr = None)
# #
# pattern = 'var data=(.+?)\n'
# raw_data = re.findall(pattern,scrapt_tag.string, re.S)
# if raw_data:
#     data = json.loads(raw_data[0])
#     print(data)
# # # cos = soup.find(class_='eoupkm71')
# # print(cos)


# driver = webdriver.Chrome(executable_path='C:/Users/emils/PycharmProjects/Development/chromedriver.exe')
# driver.get(URL)
# time.sleep(3)
# cos = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
# cos.click()
# soup = BeautifulSoup(driver.page_source,'html.parser')
# offers = soup.find('div',class_='css-jjerc6 ')
# print(offers)
# driver.quit()
# time.sleep(2)
#
# cos = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
# cos.click()
#
# offert = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div[6]/div[1]')
# print(offert.text)
#
# termin = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div[6]/div[3]')
# print(termin.text)
# playing_list = json.loads(response)
# max_time = 0
# playing_now_dict = {}
# print(playing_list)
# for playings in playing_list :
#     if int(playings['start_time']) > max_time  :
#         playing_now_dict = playings
# print(playing_now_dict.get('title', ''))
# print(playing_now_dict.get('artist', ''))



# info = soup.find_all('div',class_='css-1sxg93g')
# yeah = [cos.getText() for cos in info]

# print(yeah)











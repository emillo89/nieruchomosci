from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
from models_flat import Flats

if __name__ == '__main__':
    offers = []
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
    db = SQLAlchemy(app)
    db.create_all()

    def parse_main_page(page: int) -> list:
        URL = f'''https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wiele-lokalizacji?distanceRadius=0&page={page}&limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''

        print(URL)
        web_page = WebScrappingMainPage()
        soup = web_page.get_page(URL)
        pages = web_page.get_how_many_pages(soup)

        for page in range(1):
            soup = web_page.get_page(URL)
            links = web_page.get_links_with_main_page(soup)
        all_links = web_page.all_links
        return all_links


    def parse_page(page: int):
        all_links = parse_main_page(page)
        for url in all_links:
            try:
                site = WebScrapping()
                soup = site.get_links(url)
            except AttributeError:
                continue
            else:
                price = site.get_price(soup)
                if price == None:
                    continue
                kind_of_investment, city, province, district, street = site.get_locations(soup)
                balcony, rent, available, own, suplementary, rooms, building_material, media, car_park, remote_service,\
                    heating, windows, floor, area, type_of_building, year_of_building, market, state_of_the_building_finish,\
                    advertiser_add, elevator, equipment, security= site.show_details(soup)
                if city == None and own == None and area == None:
                    continue
                nr_offert = site.get_nr_offert(soup)
                date_addition_add = site.get_date_addition(soup)
                date_actualisation_add = site.get_date_actualisation(soup)
                print(f'''{price} - {area} - {rooms} - {own} - {year_of_building} - {available} - {rent} - {floor} - {heating} - {car_park},
                {market} - {advertiser_add} - {state_of_the_building_finish} - {city} - {province} - {district} - {street} -
                {date_addition_add}, {date_actualisation_add}, {type_of_building}, {kind_of_investment},
                {building_material} - {suplementary} - {remote_service} - {security} - {media} - {balcony} - {windows} - {
                    elevator} -
                {equipment} - {nr_offert} - - {url}''' )

                flat = site.create_new_flat(price, area, rooms, own, year_of_building, available, rent, floor, heating, car_park,
                            market, advertiser_add, state_of_the_building_finish, city, province, district, street,
                            date_addition_add, date_actualisation_add, type_of_building, kind_of_investment,
                            building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                            equipment, nr_offert, url)

                db.session.add(flat)
                db.session.commit()

    parse_page(1)
    # db.session.add_all(offers)
    # db.session.commit()











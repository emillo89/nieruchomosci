from datetime import datetime
from sqlalchemy.exc import IntegrityError

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
# from models_flat import Flats

if __name__ == '__main__':
    offers = []
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'

    db = SQLAlchemy(app)

    class Flats(db.Model):
        __tablename__ = 'property'
        id = db.Column(db.Integer, primary_key=True)
        price = db.Column(db.Float, nullable=False)
        rooms = db.Column(db.Integer, nullable=True)
        area = db.Column(db.Float, nullable=False)
        own = db.Column(db.String(100), nullable=False)
        year_of_building = db.Column(db.String(100), nullable=True)
        available = db.Column(db.String(100), nullable=True)
        rent = db.Column(db.Integer, nullable=True)
        floor = db.Column(db.String(100), nullable=True)
        heating = db.Column(db.String(100), nullable=True)
        car_park = db.Column(db.String(100), nullable=True)
        market = db.Column(db.String(100), nullable=True)
        advertiser_add = db.Column(db.String(100), nullable=True)
        state_of_the_building_finish = db.Column(db.String(100), nullable=True)
        city = db.Column(db.String(100), nullable=False)
        province = db.Column(db.String(100), nullable=True)
        district = db.Column(db.String(100), nullable=True)
        street = db.Column(db.String(100), nullable=True)
        date_addition_add = db.Column(db.DateTime, nullable=True)
        date_actualisation_add = db.Column(db.DateTime, nullable=True)
        date_add_to_database = db.Column(db.DateTime, default=datetime.utcnow)
        type_of_building = db.Column(db.String(100), nullable=True)
        kind_of_investment = db.Column(db.String(100), nullable=True)
        building_material = db.Column(db.String(100), nullable=True)
        suplementary = db.Column(db.String(100), nullable=True)
        remote_service = db.Column(db.String(100), nullable=True)
        security = db.Column(db.String(256), nullable=True)
        media = db.Column(db.String(100), nullable=True)
        balcony = db.Column(db.String(100), nullable=True)
        windows = db.Column(db.String(100), nullable=True)
        elevator = db.Column(db.String(100), nullable=True)
        equipment = db.Column(db.String(100), nullable=True)
        nr_offert = db.Column(db.String(256), nullable=True)
        contact_person  = db.Column(db.String(100), nullable=True)
        contact_number = db.Column(db.String(100), nullable=True)
        link = db.Column(db.String(256), nullable=True)


    db.create_all()


    def create_new_flat(price, area, rooms, own, year_of_building, available, rent, floor, heating, car_park,
                        market, advertiser_add, state_of_the_building_finish, city, province, district, street,
                        date_addition_add,date_actualisation_add,type_of_building, kind_of_investment,
                        building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                        equipment, nr_offert, contact_person, contact_number, link)->Flats:
        new_flat = Flats(
            price=price,
            area=area,
            rooms=rooms,
            own=own,
            year_of_building=year_of_building,
            available=available,
            rent=rent,
            floor=floor,
            heating=heating,
            car_park=car_park,
            market=market,
            advertiser_add=advertiser_add,
            state_of_the_building_finish=state_of_the_building_finish,
            city=city,
            province=province,
            district=district,
            street=street,
            date_addition_add=date_addition_add,
            date_actualisation_add=date_actualisation_add,
            type_of_building=type_of_building,
            kind_of_investment=kind_of_investment,
            building_material=building_material,
            suplementary=suplementary,
            remote_service=remote_service,
            security=security,
            media=media,
            balcony=balcony,
            windows=windows,
            elevator=elevator,
            equipment=equipment,
            nr_offert=nr_offert,
            contact_person=contact_person,
            contact_number=contact_number,
            link=link
        )
        return new_flat

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
                soup,contact_person, contact_number = site.get_links(url)
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
                {type_of_building}, {kind_of_investment}, {date_addition_add} - {date_actualisation_add}
                {building_material} - {suplementary} - {remote_service} - {security} - {media} - {balcony} - {windows} - {
                    elevator} -
                {equipment} - {nr_offert}  -{contact_person} - {contact_number} - {url}''' )

                flat = create_new_flat(price, area, rooms, own, year_of_building, available, rent, floor, heating, car_park,
                            market, advertiser_add, state_of_the_building_finish, city, province, district, street,
                            date_addition_add,date_actualisation_add,type_of_building, kind_of_investment,
                            building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                            equipment, nr_offert, contact_person, contact_number, url)
    #
                try:
                    db.session.add(flat)
                    db.session.commit()
                except TypeError:
                    continue
                except IntegrityError:
                    db.session.rollback()

    parse_page(1)
    # db.session.add_all(offers)
    # db.session.commit()











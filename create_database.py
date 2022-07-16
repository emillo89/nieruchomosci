from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import Flats
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage

if __name__ == '__main__':
    offers = []
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
    db = SQLAlchemy(app)
    # db.create_all()

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
        print(len(web_page.all_links))
        return all_links


    def parse_page(page: int):
        all_links = parse_main_page(page)
        for url in all_links:
            site = WebScrapping()
            soup = site.get_links(url)
            price = site.get_price(soup)
            kind_of_investment, city, province, district, street = site.get_locations(soup)
            balcony, rent, available, own, suplementary, rooms, building_material, media, car_park, remote_service,\
                heating, windows, floor, area, type_of_building, year_of_building, market, state_of_the_building_finish,\
                advertiser_add, elevator, equipment, security= site.show_details(soup)
            nr_offert = site.get_nr_offert(soup)
            date_addition_add = site.get_date_addition(soup)
            date_actualisation_add = site.get_date_actualisation(soup)
            print(f'{area} - {year_of_building} - {nr_offert} - {date_addition_add} - {date_actualisation_add} - {url}' )


    parse_page(1)

    # def create_new_flat(city, price, area, rooms, link, own, finishing, level, rent, parking, heating, market,
    #                     advertisement, years_of_building, province, district, settlement, street, date_add_to_date):
    #
    #     new_flat = Flats(
    #         city=city,
    #         price=price,
    #         area=area,
    #         rooms=rooms,
    #         link=link,
    #         own=own,
    #         finishing=finishing,
    #         level=level,
    #         rent=rent,
    #         parking=parking,
    #         heating=heating,
    #         market=market,
    #         advertisement=advertisement,
    #         # years_of_building=years_of_building,
    #         province=province,
    #         district=district,
    #         settlement=settlement,
    #         street=street,
    #         date_add_to_date=date_add_to_date
    #     )
        # offers.append(new_flat)


    # db.session.add_all(offers)
    # db.session.commit()











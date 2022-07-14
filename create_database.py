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
        URL = f'''https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wiele-lokalizacji?distanceRadius=0&market=ALL&
                locations=%5Bcities_6-26%2Ccities_6-38%2Ccities_6-1004%2Ccities_6-39%2Ccities_6-1%2Ccities_6-40%2Ccities_6-
                213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-204%5D&viewType=listing&limit=72&page={page}'''
        web_page = WebScrappingMainPage()
        soup = web_page.get_page(URL)
        pages = web_page.get_how_many_pages(soup)

        for page in range(3):
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
            print(price)


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











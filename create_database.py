from sqlalchemy.exc import IntegrityError
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
from models_flat import Links, Session, Flats
from sqlalchemy import update
from typing import List, Optional
from datetime import datetime
from readDatabase import ReadData

session = Session()


def parse_main_page(page: int) -> None:
    web_page = WebScrappingMainPage()
    kind_building = ['dom', 'mieszkanie']

    for kind in kind_building:
        url= f'''https://www.otodom.pl/pl/oferty/sprzedaz/{kind}/wiele-lokalizacji?distanceRadius=0&page={page}&limit=72
                 &market=ALL&locations=%5Bcities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-38%2Ccities_6-39%2Ccities
                 _6-1004%2Ccities_6-40%2Ccities_6-1%2Ccities_6-184%2Ccities_6-213%5D&viewType=listing'''
        soup = web_page.get_page(url)
        pages = web_page.get_how_many_pages(soup)

        for page in range(1, pages):
            soup = web_page.get_page(f'''https://www.otodom.pl/pl/oferty/sprzedaz/{kind}/wiele-lokalizacji?distanceRadius=0&page={page}&limit=72&market=ALL&locations=%5Bcities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-38%2Ccities_6-39%2Ccities_6-1004%2Ccities_6-40%2Ccities_6-1%2Ccities_6-184%2Ccities_6-213%5D&viewType=listing''')
            web_page.get_links_with_main_page(soup)


def check_link(check_url: str, price: float) -> Optional:
    data = ReadData('link2.db')
    df = data.query_connection_url()
    try:
        flat_id = df.index[df['url'] == check_url]
    except IndexError:
        return False
    else:
        pass



# def check_price(float_id: int, price: float) -> None:
#     flat = Flats.query.get(check_url)
#     if flat.price != price:
#         flat.price = price
#         flat.date_actualisation_add = datetime.utcnow().date()
#     session.commit()


def parse_page(page: int):
    # all_links = parse_main_page(page)
    # with open('link_offert.txt', 'r+', encoding='UTF-8') as all_links:
    session = Session()
    all_links = session.query(Links).all()
    # all_flats = session.query(Flats).all()
    for row in all_links:
        print(row.url)

        try:
            site = WebScrapping()
            soup, contact_person, contact_number = site.get_links(row.url)
            print(f'{row.id}')
        except AttributeError:
            continue
        else:
            print('3')
            price = site.get_price(soup)
            if price == None:
                continue
            # check_url = check_link(row.url, price)
            # if check_url != False:
            #     print(row.id)
            #     check_price(check_url, price)
            #     continue

            kind_of_investment, city, province, district, street = site.get_locations(soup)
            balcony, rent, roof, access, leisure_house, available, own, suplementary, numbers_of_floors, rooms,\
            building_material, media, car_park, remote_service, fence, heating, windows, neighborhood, floor, attic,\
            roofing, area, parcel_area, location, type_of_building, year_of_building, market,\
            state_of_the_building_finish, advertiser_add, elevator, equipment, security = site.show_details(soup)
            if city == None and own == None and area == None:
                continue

            nr_offert = site.get_nr_offert(soup)
            date_addition_add = site.get_date_addition(soup)
            date_actualisation_add = site.get_date_actualisation(soup)
            print(kind_of_investment)
            print(f'''{price} - {area} - {rooms} - {own} - {year_of_building} - {available} - {rent} - {floor} - {heating} - {car_park},
            {market} - {advertiser_add} - {state_of_the_building_finish} - {city} - {province} - {district} - {street} -
            {type_of_building}, {kind_of_investment}, {date_addition_add} - {date_actualisation_add}
            {building_material} - {suplementary} - {remote_service} - {security} - {media} - {balcony} - {windows} - {
                elevator} -
            {equipment} - {nr_offert}  -{contact_person} - {contact_number} - {row.url}''')

            flat = site.create_new_flat(row.id, kind_of_investment, city, area, price, rooms, own, year_of_building, available,
                                        rent, floor, heating, car_park, market, advertiser_add,
                                        state_of_the_building_finish, province, district, street, date_addition_add,
                                        date_actualisation_add, type_of_building, building_material, suplementary,
                                        remote_service, security, media, balcony, windows, elevator, equipment, roof,
                                        access, leisure_house, numbers_of_floors, fence, neighborhood, attic, roofing,
                                        parcel_area, location, contact_person, contact_number, row.url, nr_offert)

            print(flat)
            try:
                session.add(flat)
                session.commit()
                print('Działa')
            except TypeError:
                print('Nie dziala')
                continue
            except IntegrityError:
                print("yyyyy")
                session.rollback()
# parse_main_page(1)
# parse_page(1)

all_links = session.query(Flats).all()

# book = Links.query.filter_by(url="https://www.otodom.pl/pl/oferta/dom-ogrod-garaz-ochrona-prestizowe-osiedle-oporow-ID4h8cm").first()
# print(book.id)
for row in all_links[:1]:
    print(row.url)
    link = Flats.query.filter_by(url=row.url).first()


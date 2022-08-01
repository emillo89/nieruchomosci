from sqlalchemy.exc import IntegrityError
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
from models_flat import Flats, Session


session = Session()

def parse_main_page(page: int) -> list:
    web_page = WebScrappingMainPage()
    URL1 = f'''https://www.otodom.pl/pl/oferty/sprzedaz/dom/wiele-lokalizacji?distanceRadius=0&page={page}
        &limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-
        204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''
    URL2 = f'''https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wiele-lokalizacji?distanceRadius=0&page={page}
    &limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-
    204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''
    URL = [URL1, URL2]
    for kind in URL:
        soup = web_page.get_page(kind)
        pages = web_page.get_how_many_pages(soup)

        for page in range(1):
            soup = web_page.get_page(kind)
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
            balcony, rent, roof, access, leisure_house, available, own, suplementary, numbers_of_floors,rooms,\
            building_material, media, car_park, remote_service,fence, heating, windows, neighborhood, floor, attic,\
            roofing, area, parcel_area, location, type_of_building, year_of_building, market,\
            state_of_the_building_finish,advertiser_add, elevator, equipment, security= site.show_details(soup)
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

            flat = site.create_new_flat(price, area, rooms, own, year_of_building, available, rent, floor, heating, car_park,
                        market, advertiser_add, state_of_the_building_finish, city, province, district, street,
                        date_addition_add,date_actualisation_add,type_of_building, kind_of_investment,
                        building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                        equipment,roof, access, leisure_house,numbers_of_floors,fence,neighborhood,attic,roofing,
                        parcel_area, location, contact_person, contact_number, url,nr_offert)

            print(flat)
            try:
                session.add(flat)
                session.commit()
                print('Działa')
            except TypeError:
                print('Nie dziala')
                continue
            except IntegrityError:
                session.rollback()


parse_page(1)












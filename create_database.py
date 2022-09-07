from sqlalchemy.exc import IntegrityError
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
from models_flat import Session




session = Session()

def add_link_to_file(link):
    with open("link.txt", "w") as file:
        for li in link:
            file.write(li)


def parse_main_page(page: int) -> list:
    web_page = WebScrappingMainPage()
    # url1 = f'''https://www.otodom.pl/pl/oferty/sprzedaz/dom/wiele-lokalizacji?distanceRadius=0&page={page}
    #     &limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-
    #     204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''
    # url2 = f'''https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wiele-lokalizacji?distanceRadius=0&page={page}
    # &limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-
    # 204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''
    # url = [url1, url2]
    # for kind in url:
    #     print(kind)
    #     soup = web_page.get_page(kind)
    #     pages = web_page.get_how_many_pages(soup)


    kind_building = ['dom', 'mieszkanie']

    for kind in kind_building:
        url= f'''https://www.otodom.pl/pl/oferty/sprzedaz/{kind}/wiele-lokalizacji?distanceRadius=0&page={page}&limit=72
&market=ALL&locations=%5Bcities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-38%2Ccities_6-39%2Ccities_6-1004%2
Ccities_6-40%2Ccities_6-1%2Ccities_6-184%2Ccities_6-213%5D&viewType=listing'''
        soup = web_page.get_page(url)
        pages = web_page.get_how_many_pages(soup)


        for page in range(pages):
            soup = web_page.get_page(f'''https://www.otodom.pl/pl/oferty/sprzedaz/{kind}/wiele-lokalizacji?distanceRadius=0&page={page}&limit=72&market=ALL&locations=%5Bcities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-38%2Ccities_6-39%2Ccities_6-1004%2Ccities_6-40%2Ccities_6-1%2Ccities_6-184%2Ccities_6-213%5D&viewType=listing''')
            web_page.get_links_with_main_page(soup)
            print(f'''https://www.otodom.pl/pl/oferty/sprzedaz/{kind}/wiele-lokalizacji?distanceRadius=0&page={page}&limit=72&market=ALL&locations=%5Bcities_6-190%2Ccities_6-204%2Ccities_6-26%2Ccities_6-38%2Ccities_6-39%2Ccities_6-1004%2Ccities_6-40%2Ccities_6-1%2Ccities_6-184%2Ccities_6-213%5D&viewType=listing''')
    all_links = web_page.all_links

    with open('link_offert.txt', 'a', encoding='UTF-8') as file:
        for link in all_links:
            file.write(link)
            file.write('\n')
    # print(all_links)
    return all_links



    #     for page in range(pages):
    #         soup = web_page.get_page(kind)
    #         web_page.get_links_with_main_page(soup)
    # all_links = web_page.all_links
    # print(all_links)
    # return all_links


def parse_page(page: int):
    # all_links = parse_main_page(page)
    with open('link_offert.txt', 'r+', encoding='UTF-8') as all_links:

        for url in all_links:
            print(url)
            try:
                site = WebScrapping()
                soup, contact_person, contact_number = site.get_links(url)
            except AttributeError:
                continue
            else:
                price = site.get_price(soup)
                if price == None:
                    continue
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
                {equipment} - {nr_offert}  -{contact_person} - {contact_number} - {url}''')

                flat = site.create_new_flat(kind_of_investment, city, area, price, rooms, own, year_of_building, available,
                                            rent, floor, heating, car_park, market, advertiser_add,
                                            state_of_the_building_finish, province, district, street, date_addition_add,
                                            date_actualisation_add, type_of_building, building_material, suplementary,
                                            remote_service, security, media, balcony, windows, elevator, equipment, roof,
                                            access, leisure_house, numbers_of_floors, fence, neighborhood, attic, roofing,
                                            parcel_area, location, contact_person, contact_number, url, nr_offert)

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
parse_page(1)

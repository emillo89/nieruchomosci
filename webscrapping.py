from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, ElementClickInterceptedException, InvalidArgumentException
from selenium.webdriver.common.by import By
from typing import Optional, Tuple, List, Dict
from webscrapper import WebScrapper
from webscrapping_main_page import WebScrappingMainPage
from models_flat import *
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime

DETAILS = ['Powierzchnia', 'Forma własności', 'Liczba pokoi', 'Stan wykończenia', 'Piętro', 'Balkon / ogród / taras',
           'Czynsz', 'Miejsce parkingowe', 'Obsługa zdalna', 'Ogrzewanie', 'Rynek', 'Typ ogłoszeniodawcy',
           'Dostępne od', 'Rok budowy', 'Rodzaj zabudowy', 'Okna', 'Winda', 'Media', 'Zabezpieczenia', 'Wyposażenie',
           'Informacje dodatkowe', 'Materiał budynku', 'Powierzchnia działki', 'Rodzaj zabudowy', 'Liczba pięter',
           'Dom rekreacyjny', 'Dach', 'Pokrycie dachu', 'Poddasze', 'Ogrodzenie', 'Dojazd', 'Położenie', 'Okolica',
           'Informacje dodatkowe']


class WebScrapping(WebScrappingMainPage):
    def __init__(self):
        super().__init__()

    def __contact(self) -> Tuple:
        try:
            accept = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        except NoSuchElementException:
            print('No accept')
            contact_nr = None
            contact_person = None
            return contact_nr, contact_person
        else:
            accept.click()
        try:
            show_nr = self.driver.find_element(By.CSS_SELECTOR, '.phoneNumber button')
            show_nr.click()
        except NoSuchElementException:
            print('No show1')
            contact_nr = None
        except ElementClickInterceptedException:
            print("no show2")
            contact_nr = None
        except TypeError:
            print("No show3")
            contact_nr = None
        else:
            try:
                cancel = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div/span')
            except NoSuchElementException:
                print("cancel")
                pass
            else:
                cancel.click()
            try:
                contact_nr = self.driver.find_element(By.CSS_SELECTOR, '.phoneNumber a').text
            except TypeError:
                print('typeerror')
                contact_nr = None
            except NoSuchElementException:
                print("contact nosuch")
                contact_nr = None
        try:
            contact_person = self.driver.find_element(By.CSS_SELECTOR, '.css-1dihcof span').text
        except NoSuchElementException:
            print("person no such")
            contact_person = None
        return contact_nr, contact_person

    def get_links(self, url: str) -> Tuple:
        self.driver.get(url)
        contact_number, contact_person = self.__contact()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup, contact_number, contact_person

    @staticmethod
    def check_price(price: str) -> str:
        try:
            price = price.getText().replace(' ', '').split('zł')[0].replace(',', '.')
        except AttributeError:
            price = None
        if price == 'Zapytajocenę':
            price = None
        return price

    def get_price(self, soup: BeautifulSoup) -> str:
        price = soup.find('strong', class_='css-8qi9av')
        return self.check_price(price)

    @staticmethod
    def get_loc(soup_el: str) -> Tuple:
        locations = [locate.getText() for locate in soup_el]
        try:
            kind_of_investment = locations[0].split(' ')[0]
        except IndexError:
            kind_of_investment = None
        try:
            city = locations[2]
        except IndexError:
            city = None
        try:
            province = locations[1]
        except IndexError:
            province = None
        try:
            district = locations[3]
        except IndexError:
            district = None
        try:
            street = locations[-1]
        except IndexError:
            street = None
        else:
            if not street.startswith('ul.'):
                street = None
        return kind_of_investment, city, province, district, street

    def get_locations(self, soup: BeautifulSoup) -> Tuple:
        locations = soup.find_all('a', class_='css-1in5nid')
        return self.get_loc(locations)

    @staticmethod
    def take_all_details(dict: Dict) -> Dict:
        for key in DETAILS:
            try:
                dict[key]
            except KeyError:
                print('Tutaj blad?????')
                dict[key] = None
            except AttributeError:
                dict[key] = None
            else:
                # print(f"{details['Piętro']}")
                try:
                    if dict[key].endswith('m²'):
                        dict[key] = dict[key].split(' ')[0].replace(',', '.')
                    if dict[key].endswith('zł'):
                        dict[key] = dict[key].replace(' ', '').split('zł')[0]
                    elif dict[key].endswith('EUR'):
                        dict[key] = None
                    elif dict[key].endswith('$'):
                        dict[key] = None
                    else:
                        dict[key] = None
                    if dict[key] == 'zapytaj':
                        dict[key] = None
                except AttributeError:
                    dict[key] = None
                try:
                    if dict['Piętro'].split('/')[0] == 'parter':
                        cut = dict['Piętro'].split('/')
                        dict['Piętro'] = f'1/{cut[1]}'
                        # print("Udało się")
                    elif dict['Piętro'] == 'parter':
                        dict['Piętro'] = f'1'
                except IndexError:
                    dict['Piętro'] = None
                except AttributeError:
                    dict['Piętro'] = None
                except KeyError:
                    dict['Piętro'] = None
                # if details[key].endswith('Film'):
                #     details[key] = None
        print(dict)
        return dict

    def __get_details(self, soup: BeautifulSoup) -> Dict:
        search = soup.find_all('div', class_='css-1qzszy5')
        details = [info.getText() for info in search]
        details_dict = {}
        long = len(details)
        for index in range(0, long, 2):
            details_dict[details[index]] = details[index + 1]
        print(details_dict)
        return self.take_all_details(details_dict)

    def show_details(self, soup: BeautifulSoup) -> List:
        details = dict(sorted(self.__get_details(soup).items()))
        list = []
        for index in details:
            info = details[index]
            list.append(info)
        return list

    @staticmethod
    def show_offert(nr: str) -> str:
        try:
            offert_nr = nr.text.split(' ')[-1]
        except AttributeError:
            offert_nr = None
        return offert_nr

    def get_nr_offert(self, soup: BeautifulSoup) -> str:
        nr = soup.find('div', class_='css-jjerc6')
        return self.show_offert(nr)

    @staticmethod
    def show_date(date) -> Optional:
        now = datetime.today().date()
        try:
            date_info = date.text.split(' ')
            time_ago = int(date_info[-3])
            time_unit = date_info[-2]
        except TypeError and ValueError:
            return
        else:
            if time_ago == None and time_unit == None:
                return
            if time_ago == None:
                time_ago = 1
            if time_unit == 'sekunda' or time_unit == 'sekundę' or time_unit == 'sekund' or time_unit == 'sekundy':
                return now - timedelta(seconds=int(time_ago))
            elif time_unit == 'minut' or time_unit == 'minuty' or time_unit == 'minutę':
                return now - timedelta(minutes=int(time_ago))
            elif time_unit == 'godzinę' or time_unit == 'godzin' or time_unit == 'godziny':
                return now - timedelta(hours=int(time_ago))
            elif time_unit == 'dni' or time_unit == 'dzień':
                return now - timedelta(days=int(time_ago))
            elif time_unit == 'miesiąc' or time_unit == 'miesiące' or time_unit == 'miesięcy':
                return now - relativedelta(months=int(time_ago))
            elif time_unit == 'rok' or time_unit == 'lata' or time_unit == 'lat':
                return now - relativedelta(years=int(time_ago))
            else:
                return

    def get_date_addition(self, soup: BeautifulSoup) -> str:
        date_addition = soup.find('div', class_='css-atkgr')
        return self.show_date(date_addition)

    def get_date_actualisation(self, soup: BeautifulSoup):
        date_actualisation = soup.find('div', class_='css-wlnxoe')
        return self.show_date(date_actualisation)

    def create_new_flat(self, kind_of_investment, city, area, price, rooms, own, year_of_building, available, rent,
                        floor, heating, car_park, market, advertiser_add, state_of_the_building_finish, province,
                        district, street, date_addition_add, date_actualisation_add, type_of_building,
                        building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                        equipment, roof, access, leisure_house, numbers_of_floors, fence, neighborhood, attic, roofing,
                        parcel_area, location, contact_person, contact_number, url, nr_offert) -> Flats:

        new_flat = Flats(
            kind_of_investment=kind_of_investment,
            city=city,
            area=area,
            price=price,
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
            province=province,
            district=district,
            street=street,
            date_addition_add=date_addition_add,
            date_actualisation_add=date_actualisation_add,
            type_of_building=type_of_building,
            building_material=building_material,
            suplementary=suplementary,
            remote_service=remote_service,
            security=security,
            media=media,
            balcony=balcony,
            windows=windows,
            elevator=elevator,
            equipment=equipment,
            roof=roof,
            access=access,
            leisure_house=leisure_house,
            numbers_of_floors=numbers_of_floors,
            fence=fence,
            neighborhood=neighborhood,
            attic=attic,
            roofing=roofing,
            parcel_area=parcel_area,
            location=location,
            contact_person=contact_person,
            contact_number=contact_number,
            url=url,
            nr_offert=nr_offert
        )

        return new_flat

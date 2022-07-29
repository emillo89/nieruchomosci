import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webscrapping_main_page import WebScrappingMainPage

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from datetime import datetime

'''Dodac to'''
DETAILS = ['Powierzchnia','Forma własności','Liczba pokoi', 'Stan wykończenia','Piętro', 'Balkon / ogród / taras',
           'Czynsz','Miejsce parkingowe','Obsługa zdalna','Ogrzewanie','Rynek', 'Typ ogłoszeniodawcy','Dostępne od',
           'Rok budowy','Rodzaj zabudowy','Okna','Winda','Media','Zabezpieczenia','Wyposażenie','Informacje dodatkowe',
           'Materiał budynku', 'Powierzchnia działki','Rodzaj zabudowy','Liczba pięter','Dom rekreacyjny','Dach', 'Pokrycie dachu',
           'Poddasze', 'Ogrodzenie', 'Dojazd', 'Położenie', 'Okolica', 'Informacje dodatkowe']

class House(WebScrappingMainPage):
    def __init__(self):
        super().__init__()

    def __contact(self):
        accept = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        accept.click()
        try:
            show_nr = self.driver.find_element(By.CSS_SELECTOR, '.phoneNumber button')
            show_nr.click()
        except NoSuchElementException:
            contact_nr = None
        except ElementClickInterceptedException:
            contact_nr = None
        except TypeError:
            contact_nr = None
        else:
            try:
                cancel = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div/span')
            except NoSuchElementException:
                contact_nr = self.driver.find_element(By.CSS_SELECTOR, '.phoneNumber a').text
            else:
                cancel.clic()
        contact_person = self.driver.find_element(By.CSS_SELECTOR, '.css-1dihcof span').text
        return contact_nr, contact_person

    def get_links(self, url):
        self.driver.get(url)
        contact_number, contact_person = self.__contact()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup, contact_number, contact_person

    @staticmethod
    def check_price(price):
            try:
                price = price.getText().replace(' ', '').split('zł')[0].replace(',','.')
            except AttributeError:
                price = None
            if price == 'Zapytajocenę':
                price = None
            return price

    def get_price(self, soup):
        price = soup.find('strong', class_='css-8qi9av')
        return self.check_price(price)

    @staticmethod
    def get_loc(soup_el):
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

    def get_locations(self, soup):
        locations = soup.find_all('a', class_='css-1in5nid')
        return self.get_loc(locations)

    @staticmethod
    def take_all_details(dict):
            for key in DETAILS:
                try:
                    dict[key]
                except KeyError:
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
            return dict

    def __get_details(self, soup):
        search = soup.find_all('div',class_='css-1qzszy5')
        details = [info.getText() for info in search]
        details_dict = {}
        long = len(details)
        for index in range(0, long, 2):
            details_dict[details[index]] = details[index + 1]
        return self.take_all_details(details_dict)

    def show_details(self, soup):
        details = dict(sorted(self.__get_details(soup).items()))
        list = []
        for index in details:
            info = details[index]
            list.append(info)
        return list

    @staticmethod
    def show_offert(nr):
            try:
                offert_nr = nr.text.split(' ')[-1]
            except AttributeError:
                offert_nr = None
            return offert_nr

    def get_nr_offert(self,soup):
        nr = soup.find('div', class_='css-jjerc6')
        return self.show_offert(nr)

    @staticmethod
    def show_date(date):
        unit = ['sekunda', 'sekundy', 'sekund', 'minutę', 'minuty', 'minut', 'minuta', 'godzina', 'godzin',
                'godziny', 'dzień', 'dni', 'miesiąc',
                'miesiące', 'miesięcy', 'rok', 'lata']
        now = datetime.today().date()
        try:
            date_info = date.text.split(' ')
            time_ago = int(date_info[-3])
            time_unit = date_info[-2]
        except TypeError and ValueError:
            return
        else:
            if time_ago == None or time_unit == None:
                return
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

    def get_date_actualisation(self, soup):
        date_actualisation = soup.find('div', class_='css-zojvsz')
        return self.show_date(date_actualisation)


url = 'https://www.otodom.pl/pl/oferta/atrakcyjna-cena-komfortowy-dom-os-zodiak-186m2-ID4gFc0'
service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)

time.sleep(1)
accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
accept.click()
soup = BeautifulSoup(driver.page_source, 'lxml')


def cosnietak(dict):
    for key in DETAILS:

        try:
            dict[key]
        except KeyError:
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
    return dict

def get_details(soup):
    search = soup.find_all('div',class_='css-1qzszy5')
    details = [info.getText() for info in search]
    details_dict = {}
    long = len(details)
    for index in range(0, long, 2):
        details_dict[details[index]] = details[index + 1]

    return cosnietak(details_dict)

def show_details(soup):
    details = dict(sorted(get_details(soup).items()))
    print(details)
    print(len(details))
    list = []
    for index in details:
        info = details[index]
        list.append(info)
    return list
show = show_details(soup)
print(show)

'''Dodac elementy'''
balcony, rent, roof, access,leisure_house, available, own, suplementary, numbers_of_floors, rooms, building_material, media, car_park, remote_service,\
    fence, heating, windows, neighborhood, floor, attic, roofing, area, parcel_area, location, type_of_building, year_of_building, market, state_of_the_building_finish,\
    advertiser_add, elevator, equipment, security= show_details(soup)
'''to tez'''
print(balcony, rent, roof, access,leisure_house, available, own, suplementary, numbers_of_floors, rooms, building_material, media, car_park, remote_service,\
    fence, heating, windows, neighborhood, floor, attic, roofing, area, parcel_area, location, type_of_building, year_of_building, market, state_of_the_building_finish,\
    advertiser_add, elevator, equipment, security)

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Flats(Base):
    __tablename__ = 'property'
    id = Column(Integer(), primary_key=True)
    price = Column(Float(), nullable=False)
    rooms = Column(Integer(), nullable=True)
    area = Column(Float(), nullable=False)
    own = Column(String(100), nullable=False)
    year_of_building = Column(String(100), nullable=True)
    available = Column(String(100), nullable=True)
    rent = Column(Integer, nullable=True)
    floor = Column(String(100), nullable=True)
    heating = Column(String(100), nullable=True)
    car_park = Column(String(100), nullable=True)
    market = Column(String(100), nullable=True)
    advertiser_add = Column(String(100), nullable=True)
    state_of_the_building_finish = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    date_addition_add = Column(DateTime, nullable=True)
    date_actualisation_add = Column(DateTime, nullable=True)
    date_add_to_database = Column(DateTime, default=datetime.utcnow().date())
    type_of_building = Column(String(100), nullable=True)
    kind_of_investment = Column(String(100), nullable=True)
    building_material = Column(String(100), nullable=True)
    suplementary = Column(String(100), nullable=True)
    remote_service = Column(String(100), nullable=True)
    security = Column(String(256), nullable=True)
    media = Column(String(100), nullable=True)
    balcony = Column(String(100), nullable=True)
    windows = Column(String(100), nullable=True)
    elevator = Column(String(100), nullable=True)
    equipment = Column(String(100), nullable=True)
    nr_offert = Column(String(256), nullable=True, unique=True)
    contact_person = Column(String(100), nullable=True)
    contact_number = Column(String(100), nullable=True)
    link = Column(String(256), nullable=True)


engine = create_engine('sqlite:///flats.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

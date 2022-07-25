import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webscrapping_main_page import WebScrappingMainPage
from decoration_function import check_price, check_location, take_details, take_all_details, show_offert, show_data
from models_flat import *


class WebScrapping(WebScrappingMainPage):
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
            contact_nr = self.driver.find_element(By.CSS_SELECTOR, '.phoneNumber a').text

        contact_person = self.driver.find_element(By.CSS_SELECTOR, '.css-1dihcof span').text
        return contact_nr, contact_person

    def get_links(self, url):
        self.driver.get(url)
        contact_number, contact_person = self.__contact()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup, contact_number, contact_person


    @check_price
    def get_price(self, soup):
        price = soup.find('strong', class_='css-8qi9av')
        return price

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

    @take_all_details
    def __get_details(self, soup):
        search = soup.find_all('div',class_='css-1qzszy5')
        details = [info.getText() for info in search]
        details_dict = {}
        long = len(details)
        for index in range(0, long, 2):
            details_dict[details[index]] = details[index + 1]
        return details_dict

    def show_details(self, soup):
        details = dict(sorted(self.__get_details(soup).items()))
        list = []
        for index in details:
            info = details[index]
            list.append(info)
        return list

    @show_offert
    def get_nr_offert(self,soup):
        nr_offert = soup.find('div', class_='css-jjerc6')
        return nr_offert.text

    @show_data
    def get_date_addition(self, soup: BeautifulSoup) -> str:
        date_addition = soup.find('div', class_='css-atkgr')
        return date_addition.text

    @show_data
    def get_date_actualisation(self, soup):
        date_actualisation = soup.find('div', class_='css-zojvsz')
        return date_actualisation.text

    def create_new_flat(self, price, area, rooms, own, year_of_building, available, rent, floor, heating, car_park,
                        market, advertiser_add, state_of_the_building_finish, city, province, district, street,
                        date_addition_add, date_actualisation_add, type_of_building, kind_of_investment,
                        building_material, suplementary, remote_service, security, media, balcony, windows, elevator,
                        equipment, nr_offert, link)->Flats:
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
            link=link
        )
        return new_flat













# url = 'https://www.otodom.pl/pl/oferta/unikatowe-mieszkanie-z-widokiem-na-centrum-ID4hom3'
# service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.get(url)
# time.sleep(0.5)
# soup = BeautifulSoup(driver.page_source, 'lxml')
#
# info = soup.find_all('a', class_='css-1in5nid')
# locations = [locate.getText() for locate in info]
# kind_of_investment = locations[0].split(' ')[0]
# city = locations[2]
# province = locations[1]
# district = locations[3]
# street = locations[-1]
# print(f'{city} - {province} - {street}')
# rooms = soup.find_all('div',class_='css-1qzszy5')
# details = [cos.getText() for cos in rooms]
# long = len(details)
# new_dict = {}
# # for index in range(0,long,2):
# #     new_dict[details[index]] = details[index+1]
# # print(new_dict)
#
#
# # print(details)
# try:
#     accept = soup.find('button', '#onetrust-accept-btn-handler')
# except NoSuchElementException:
#     accept = None
# else:
#     accept.click()

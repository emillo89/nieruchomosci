import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webscrapping_main_page import WebScrappingMainPage
from decoration_function import check_price, check_location, take_details, take_all_details, show_offert, show_data


class WebScrapping(WebScrappingMainPage):

    def get_links(self, url):
        # super().get_page(url)
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        return soup

    @check_price
    def get_price(self, soup):
        price = soup.find('strong', class_='css-8qi9av').getText().replace(' ', '').split('zł')[0]
        return price

    @check_location
    def get_locations(self, soup):
        locations = soup.find_all('a', class_='css-1in5nid')
        return locations

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
    def get_date_addition(self, soup):
        date_addition = soup.find('div', class_='css-atkgr')
        return date_addition.text

    @show_data
    def get_date_actualisation(self, soup):
        date_actualisation = soup.find('div', class_='css-zojvsz')
        return date_actualisation.text













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
# for index in range(0,long,2):
#     new_dict[details[index]] = details[index+1]
# print(new_dict)
#
#
# print(details)


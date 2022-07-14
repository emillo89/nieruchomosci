import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webscrapping_main_page import WebScrappingMainPage
from decoration_function import check_price


# def check_price(func):
#     def wrapper(*args):
#         price = func(*args)
#         if price == 'Zapytajocenę':
#             price = None
#         return price
#     return wrapper


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






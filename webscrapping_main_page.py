import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebScrappingMainPage:

    def __init__(self):
        self.all_links = []

    def get_page(self, url):
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        return soup

    def get_how_many_pages(self, soup):
        page_buttons = soup.select('.css-12q40o1 nav button')
        pages = int([button.text for button in page_buttons if button.text != ''][-1])
        return pages

    def get_links_with_main_page(self, soup):
        links = soup.find_all('a', class_='css-rvjxyq')
        for link in links:
            if link['href'].startswith('/'):
                link = f"https://www.otodom.pl{link['href']}"
                if link not in self.all_links:
                    self.all_links.append(link)
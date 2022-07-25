import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebScrapper:
    def __init__(self):
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(3)
        self.driver.maximize_window()

    def get_page(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup


class WebScrappingMainPage(WebScrapper):

    def __init__(self):
        super().__init__()
        self.all_links = []

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
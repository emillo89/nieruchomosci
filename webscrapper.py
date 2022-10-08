from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebScrapper:
    def __init__(self) -> None:
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
        # self.driver = webdriver.Chrome(service=service, options=option)
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(3)
        self.driver.maximize_window()

    def get_page(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup

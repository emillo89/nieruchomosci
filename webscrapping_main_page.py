from webscrapper import WebScrapper
from bs4 import BeautifulSoup
from models_flat import Session, Links


class WebScrappingMainPage(WebScrapper):

    def __init__(self):
        super().__init__()
        self.all_links = []

    @staticmethod
    def get_how_many_pages(soup: BeautifulSoup) -> int:
        page_buttons = soup.select('.css-12q40o1 nav button')
        print(page_buttons)
        pages = int([button.text for button in page_buttons if button.text != ''][-1])
        return pages

    def get_links_with_main_page(self, soup: BeautifulSoup) -> None:
        url = []
        links = soup.find_all('a', class_='css-b2mfz3')
        for link in links:
            if link['href'].startswith('/'):
                link = f"https://www.otodom.pl{link['href']}"
                url_data = Links(
                    url = link,
                    active = True
                )
                url.append(url_data)
                if link not in self.all_links:
                    self.all_links.append(url_data)
        session = Session()
        session.add_all(url)
        session.commit()

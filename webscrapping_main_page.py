from webscrapper import WebScrapper


class WebScrappingMainPage(WebScrapper):

    def __init__(self):
        super().__init__()
        self.all_links = []

    @staticmethod
    def get_how_many_pages(soup):
        page_buttons = soup.select('.css-12q40o1 nav button')
        pages = int([button.text for button in page_buttons if button.text != ''][-1])
        return pages

    def get_links_with_main_page(self, soup):
        links = soup.find_all('a', class_='css-b2mfz3')
        for link in links:
            if link['href'].startswith('/'):
                link = f"https://www.otodom.pl{link['href']}"
                if link not in self.all_links:
                    self.all_links.append(link)


import requests
from bs4 import BeautifulSoup


def parse_price(price):
    return price.replace(' ', '').replace('zł', '')


def change_zapytaj(text):
    if text == 'zapytaj':
        text = None
    return text


def check_price(text):
    if text == 'Zapytajocenę':
        return True
    return False


def page(number, i):
    URL = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie'
    resonse = requests.get(f'{URL}/{i}?page={number}')
    content = resonse.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def parse_link(link):
    response = requests.get(link)
    content = response.text
    soup = BeautifulSoup(content,'html.parser')
    return soup
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


url = 'https://www.otodom.pl/pl/oferta/unikatowe-mieszkanie-z-widokiem-na-centrum-ID4hom3'
service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(0.5)
soup = BeautifulSoup(driver.page_source, 'lxml')

info = soup.find_all('a', class_='css-1in5nid')
locations = [locate.getText() for locate in info]
kind_of_investment = locations[0].split(' ')[0]
city = locations[2]
province = locations[1]
district = locations[3]
street = locations[-1]
print(f'{city} - {province} - {street}')
rooms = soup.find_all('div',class_='css-1qzszy5')
details = [cos.getText() for cos in rooms]
long = len(details)
new_dict = {}
for index in range(0,long,2):
    new_dict[details[index]] = details[index+1]
print(new_dict)


area_name = soup.find_all('div', class_='css-1h52dri')
a = [area.getText() for area in area_name]
print(f'yyy = {a}')




print(details)

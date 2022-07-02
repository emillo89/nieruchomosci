import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://www.otodom.pl')

"""Privace button"""
# full_window = driver.find_element(By.XPATH, '')
time.sleep(2)
accept_privacy = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
accept_privacy.click()
time.sleep(2)

"""Find element"""

find_location = driver.find_element(By.XPATH, '//*[@id="location"]/div[2]')
time.sleep(2)
find_location.click()
time.sleep(1)
your_location = driver.find_element(By.XPATH, '//*[@id="location-picker-input"]')
your_location.send_keys('Warszawa')
time.sleep(1)
mark_location = driver.find_element(By.XPATH, '//*[@id="__next"]/main/section/div/form/div/div[1]/div[3]/div/div[1]/div/div[2]/ul/li[1]/label[2]/span[1]/strong')
mark_location.click()
time.sleep(1)
# min_price = driver.find_element(By.XPATH,'//*[@id="priceMin"]')
# min_price.send_keys(5000)
# time.sleep(1)
# max_price = driver.find_element(By.XPATH, '//*[@id="priceMax"]')
# max_price.send_keys(80000)
# time.sleep(1)
# min_area = driver.find_element(By.XPATH, '//*[@id="areaMin"]')
# min_area.send_keys(30)
# time.sleep(1)
# max_area = driver.find_element(By.XPATH,'//*[@id="areaMax"]')
# max_area.send_keys(400)
# time.sleep(1)
search = driver.find_element(By.XPATH, '//*[@id="search-form-submit"]')
search.click()
time.sleep(2)
cancel = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div/span')
cancel.click()


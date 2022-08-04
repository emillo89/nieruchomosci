# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
#
# url=f'''https://www.otodom.pl/pl/oferty/sprzedaz/dom/wiele-lokalizacji?distanceRadius=0&page=1
#         &limit=36&market=ALL&locations=%5Bcities_6-1%2Ccities_6-40%2Ccities_6-213%2Ccities_6-184%2Ccities_6-190%2Ccities_6-
#         204%2Ccities_6-26%2Ccities_6-1004%2Ccities_6-38%2Ccities_6-39%5D&viewType=listing'''
# service = Service(executable_path="C:/Users/emils/PycharmProjects/Development/chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'lxml')
# # print(soup)
#
# links = soup.find_all('a', class_='css-b2mfz3')
# for link in links:
#     print(link["href"])
#
# a = '100000EURo'
#
# if a.endswith('EUR'):
#     print('dada')


link = ['a', 'b']

def add_link(link):
    with open("nowy.txt", "a", encoding="UTF-8") as file:
        for li in link:
            file.write(li)
            file.write('\n')
add_link(link)

def use_link():
    with open('nowy.txt', "r", encoding="UTF-8") as file:
        for li in file:
            print(li)

# use_link()
for i in link:
    print(i)


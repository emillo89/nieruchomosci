from sqlalchemy.testing import db

from models_flat import Links
from models_flat import Session
import numpy as np
#
session = Session()
# link = []
# #
# with open('emil', 'r') as file:
#     text = file.readlines()
#     for l in text:
#         li = Links(link=l)
#         link.append(li)
# # print(link)
#
# session.add_all(link)
# session.commit()

# list = [1,2,3,4,5,6,7,8,9]
#
# for i in list:
#     if i == 5:
#         continue
#     print(i)


from readDatabase import ReadData
from datetime import datetime
from sqlalchemy import update

# data = ReadData('offert.db')
# df = data.query_connection()
# price_per_1m2 = (df['price'] // df['area']).apply(np.ceil)
# df.insert(6, 'price_per_1m2', price_per_1m2)
#
# print(df)
# print(df['url'])
# for i in df['url']:
#     if i == 'https://www.otodom.pl/pl/oferta/przestronny-ekskluzywny-apartament-w-centrum-ID3ybQb':
#         print('wow')
# search = df.index[df['link'] == 'https://www.otodom.pl/pl/oferta/nowe-domy-143m2-oddanie-iv-kwartal-2022-ID4eeqR'][0]
# print(df.loc[search]['price'])
# print(df.loc[search]['price_per_1m2'])
# up = (update)
# update('link').values('price'=1990000)
# df.at[search,'date_actualisation_add'] = datetime.utcnow().date()

# df.at[search,'price'] = 1999000
# df.at[search,'date_actualisation_add'] = datetime.utcnow().date()

# session.commit()
# print(df.loc[search]['price'])
# print(df.loc[search]['price_per_1m2'])

from models_flat import Flats, Links, Session, engine
from readDatabase import ReadData

data = ReadData('link2.db')
df = data.query_connection_url()
print(df)

# local_session = Session(bind=engine)
# # link = local_session.query(Links).all()
# # for i in link:
# #     print(i.url)
# link = local_session.query(Links).filter(Links.url=='https://www.otodom.pl/pl/oferta/piekny-dom-na-morasku-ID4hTra')
#
# print(f'cos inneg {link["id"]}')
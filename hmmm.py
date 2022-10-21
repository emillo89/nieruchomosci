from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime




#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100),nullable=False)
#     #add parent relationship
#     posts = relationship('BlogPost', back_populates='author')
#
#
#
# class BlogPost(Base):
#     __tablename__ = "blog_posts"
#     id = Column(Integer, primary_key=True)
#     #add child relationship
#     author_id = Column(Integer, ForeignKey('users.id'))
#     author = relationship('User', back_populates='posts')
# #
# # engine = create_engine('sqlite:///link44.db', echo=True)
# # Base.metadata.create_all(bind=engine)
# # Session = sessionmaker(bind=engine)

from sqlalchemy.exc import IntegrityError
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
# from models_flat import Links, Session, Flats
# from sqlalchemy import update
# from typing import List, Optional
# from datetime import datetime
# from readDatabase import ReadData
# print('adasdad')
# session = Session()
# all_links = session.query(Links).all()
#
# for row in all_links:
#     print(row.url)
from sqlalchemy.exc import IntegrityError
from webscrapping import WebScrapping
from webscrapping_main_page import WebScrappingMainPage
from models_flat import Links, Session, Flats, LinksDim
from sqlalchemy import update
from typing import List, Optional
from datetime import datetime
from readDatabase import ReadData
import pandas as pd
import sqlalchemy as sqla
# from models_flat import Session, LinksDim


def create_scd(flat: object, flag=0) -> object:
    flat_scd = LinksDim(
        link_id=flat.link_id,
        kind_of_investment=flat.kind_of_investment,
        city=flat.city,
        area=flat.area,
        price=flat.price,
        rooms=flat.rooms,
        own=flat.own,
        year_of_building=flat.year_of_building,
        available=flat.available,
        rent=flat.rent,
        floor=flat.floor,
        heating=flat.heating,
        car_park=flat.car_park,
        market=flat.market,
        advertiser_add=flat.advertiser_add,
        state_of_the_building_finish=flat.state_of_the_building_finish,
        province=flat.province,
        district=flat.district,
        street=flat.street,
        date_addition_add=flat.date_addition_add,
        date_actualisation_add=flat.date_actualisation_add,
        type_of_building=flat.type_of_building,
        building_material=flat.building_material,
        suplementary=flat.suplementary,
        remote_service=flat.remote_service,
        security=flat.security,
        media=flat.media,
        balcony=flat.balcony,
        windows=flat.windows,
        elevator=flat.elevator,
        equipment=flat.equipment,
        roof=flat.roof,
        access=flat.access,
        leisure_house=flat.leisure_house,
        numbers_of_floors=flat.numbers_of_floors,
        fence=flat.fence,
        neighborhood=flat.neighborhood,
        attic=flat.attic,
        roofing=flat.roofing,
        parcel_area=flat.parcel_area,
        location=flat.location,
        contact_person=flat.contact_person,
        contact_number=flat.contact_number,
        url=flat.url,
        nr_offert=flat.nr_offert,
        flag=flag
    )

    return flat_scd

session = Session()
flat = ReadData('link4.db')
links = flat.query_connection_url()
flats = flat.query_connection()
dim = flat.query_connection_urldim()

wow = flat.show_scd(flats, dim)
print(wow)

# url = 'https://www.otodom.pl/pl/oferta/nowoczesne-domy-z-darmowym-ogrzewaniem-dostepne-ID4hqMG'
# flat_check = session.query(Flats).filter_by(url=url).first()
# print(flat_check.link_id)
# price = 20
#
# if flat_check.price != price:
#     new_dim = create_scd(flat_check, flag=0)
#     flat_check.price = price
#     flat_check.date_actualisation_add = datetime.utcnow().date()
#     all = [flat_check, new_dim]
#     session.add_all(all)
#     session.commit()
#
#
# def show_scd(flats, dim):
#     # df_merge_col = pd.merge(flats, dim, left_on='link_id', right_on='link_id', how='left')
#     df_allrows = [flats, dim]
#     df_allrows_concat = pd.concat(df_allrows).sort_values(['link_id'], ascending=(True))
#     return df_allrows_concat
#
#
# print(show_scd(flats, dim))

# #Get max
#
# #filter only Current records from Dimension
# flats_current = flats[flats['flag'] == 1]
#
# # Left Join dataframes on keyfields
# df_merge_col = pd.merge(links, flats, left_on='id', right_on='id', how='left')
#
# #fix Datatypes
#
# #Identify new records By checking if DimKey IsNull
# new_records_filter = pd.isnull(df_merge_col['flag'])
# # print(new_records_filter)
# #create dataframe for new records
# df_new_records = df_merge_col[new_records_filter]
# print(df_new_records)
#
# #join dataframe and exclude duplicates (remove new records)
# df_excluding_new = pd.concat([df_merge_col, df_new_records]).drop_duplicates(keep=False)
# print(df_excluding_new)
#
# #identify SCD Type 2 records By comparing SCD2 fields in source and dimension
# df_scd2_records = df_excluding_new[df_excluding_new['url_x'] != df_excluding_new['url_y']]
#
# df_excluding_new_scd2 = pd.concat([df_excluding_new, df_scd2_records])
# df_scdold = df_excluding_new_scd2
# df_scdnew_final = df_excluding_new_scd2
# df_New_rename = df_excluding_new_scd2
# # df_New_rename['price'] =


# join_df = pd.merge(links, flats, left_on='id', right_on='id', how='left')
# print(join_df)


# for ind, row in flats.iterrows():
#     print(f'ind = {ind}, row= {row.id}')
#     upd=sqla.sql.update(datatable)\
#         .values({'flag':0})\
#         .where (sqla.and_(datatable.c.id==row.id))
#     session.execute(upd)
# session.flush()
# session.commit()











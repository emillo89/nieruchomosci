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
from models_flat import Links, Session, Flats
from sqlalchemy import update
from typing import List, Optional
from datetime import datetime
from readDatabase import ReadData
print('adasdad')
session = Session()
all_links = session.query(Links).all()

for row in all_links:
    print(row.url)









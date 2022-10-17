from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Flats(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('link.id'))
    parent = relationship('Links', back_populates='children')
    kind_of_investment = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    area = Column(Float(), nullable=False)
    price = Column(Float(), nullable=False)
    rooms = Column(Integer(), nullable=True)
    own = Column(String(100), nullable=True)
    year_of_building = Column(String(100), nullable=True)
    available = Column(String(100), nullable=True)
    rent = Column(Integer(), nullable=True)
    floor = Column(String(100), nullable=True)
    heating = Column(String(100), nullable=True)
    car_park = Column(String(100), nullable=True)
    market = Column(String(100), nullable=True)
    advertiser_add = Column(String(100), nullable=True)
    state_of_the_building_finish = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    date_addition_add = Column(DateTime, nullable=True)
    date_actualisation_add = Column(DateTime, nullable=True)
    date_add_to_database = Column(DateTime, default=datetime.utcnow().date())
    type_of_building = Column(String(100), nullable=True)
    building_material = Column(String(100), nullable=True)
    suplementary = Column(String(100), nullable=True)
    remote_service = Column(String(100), nullable=True)
    security = Column(String(256), nullable=True)
    media = Column(String(100), nullable=True)
    balcony = Column(String(100), nullable=True)
    windows = Column(String(100), nullable=True)
    elevator = Column(String(100), nullable=True)
    equipment = Column(String(100), nullable=True)
    roof = Column(String(100), nullable=True)
    access = Column(String(100), nullable=True)
    leisure_house = Column(String(100), nullable=True)
    numbers_of_floors = Column(String(100), nullable=True)
    fence = Column(String(100), nullable=True)
    neighborhood = Column(String(100), nullable=True)
    attic = Column(String(100), nullable=True)
    roofing = Column(String(100), nullable=True)
    parcel_area = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    contact_person = Column(String(100), nullable=True)
    contact_number = Column(String(100), nullable=True)
    url = Column(String(256), nullable=True)
    nr_offert = Column(String(256), nullable=True)
    flag = Column(Integer(), default=1)



# engine = create_engine('sqlite:///offert.db', echo=True)
# Base.metadata.create_all(bind=engine)
# Session = sessionmaker(bind=engine)


class Links(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    url = Column(String(256), nullable=True, unique=True)
    active = Column(String(256), nullable=True, default=True)
    children = relationship('Flats', back_populates='parent')


# class History(Base):
#     __tablename__ = 'history'



engine = create_engine('sqlite:///link3.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

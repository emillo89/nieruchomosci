from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Flats(Base):
    __tablename__ = 'property'
    id = Column(Integer(), primary_key=True)
    price = Column(Float(), nullable=False)
    rooms = Column(Integer(), nullable=True)
    area = Column(Float(), nullable=False)
    own = Column(String(100), nullable=False)
    year_of_building = Column(String(100), nullable=True)
    available = Column(String(100), nullable=True)
    rent = Column(Integer, nullable=True)
    floor = Column(String(100), nullable=True)
    heating = Column(String(100), nullable=True)
    car_park = Column(String(100), nullable=True)
    market = Column(String(100), nullable=True)
    advertiser_add = Column(String(100), nullable=True)
    state_of_the_building_finish = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    province = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    date_addition_add = Column(DateTime, nullable=True)
    date_actualisation_add = Column(DateTime, nullable=True)
    date_add_to_database = Column(DateTime, default=datetime.utcnow().date())
    type_of_building = Column(String(100), nullable=True)
    kind_of_investment = Column(String(100), nullable=True)
    building_material = Column(String(100), nullable=True)
    suplementary = Column(String(100), nullable=True)
    remote_service = Column(String(100), nullable=True)
    security = Column(String(256), nullable=True)
    media = Column(String(100), nullable=True)
    balcony = Column(String(100), nullable=True)
    windows = Column(String(100), nullable=True)
    elevator = Column(String(100), nullable=True)
    equipment = Column(String(100), nullable=True)
    nr_offert = Column(String(256), nullable=True, unique=True)
    contact_person = Column(String(100), nullable=True)
    contact_number = Column(String(100), nullable=True)
    link = Column(String(256), nullable=True)


engine = create_engine('sqlite:///flats.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

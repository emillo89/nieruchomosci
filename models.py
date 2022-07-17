# from datetime import datetime
from create_database import db

price = site.get_price(soup)
            kind_of_investment, city, province, district, street = site.get_locations(soup)
            balcony, rent, available, own, suplementary, rooms, building_material, media, car_park, remote_service,\
                heating, windows, floor, area, type_of_building, year_of_building, market, state_of_the_building_finish,\
                advertiser_add, elevator, equipment, security= site.show_details(soup)
            nr_offert = site.get_nr_offert(soup)
            date_addition_add = site.get_date_addition(soup)
            date_actualisation_add = site.get_date_actualisation(soup)
class Flats(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    rooms = db.Column(db.Integer,nullable=True)
    link = db.Column(db.String(256), nullable=True)
    own = db.Column(db.String(100), nullable=True)
    finishing = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(10), nullable=True)
    rent = db.Column(db.Integer, nullable=True)
    parking = db.Column(db.String(100), nullable=True)
    heating = db.Column(db.String(100), nullable=True)
    market = db.Column(db.String(100), nullable=True)
    advertisement = db.Column(db.String(100), nullable=True)
    # years_of_building = db.Column(db.DateTime, nullable=True)
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    settlement = db.Column(db.String(100))
    street = db.Column(db.String(100))
    date_add_to_date = db.Column(db.DateTime, default=datetime.utcnow)
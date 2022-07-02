# from search_flats import parse_page
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flats.db'
# db = SQLAlchemy(app)
#
# class Flats(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     area = db.Column(db.Integer, nullable=False)
#     rooms = db.Column(db.Integer, nullable=False)
#
#
# db.create_all()
#
#
# # parse_page(1)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#

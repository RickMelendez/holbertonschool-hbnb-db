""" Another way to run the app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from src.models.user import User
from src.models.country import Country
from src.models.city import City
from src.models.place import Place
from src.models.review import Review
from src.models.amenity import Amenity, PlaceAmenity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
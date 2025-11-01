from db import db
from datetime import datetime

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(10))
    time_in = db.Column(db.DateTime, default=datetime.now)
    time_out = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    level = db.Column(db.Integer)
    area = db.Column(db.String(1))
    space = db.Column(db.Integer)

class ParkingSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    area = db.Column(db.String(1))
    space = db.Column(db.Integer)
    is_occupied = db.Column(db.Boolean, default=False)
    plate_number = db.Column(db.String(10))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
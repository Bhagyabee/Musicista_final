from musicista import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     location = db.Column(db.String(255))
#     artist_name = db.Column(db.String(255))
#     event_date = db.Column(db.Date)
#
#     event_name = db.Column(db.String(255))
#     live_demo = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='bookings')
#
#
#     def __init__(self, location, artist_name, event_date, event_name, live_demo):
#         self.location = location
#         self.artist_name = artist_name
#         self.event_date = event_date
#
#         self.event_name = event_name
#         self.live_demo = live_demo


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.String(10000))
    live = db.Column(db.String(10))
    event = db.Column(db.String(10000))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone_no = db.Column(db.Integer)
    email = db.Column(db.String(150))
    message = db.Column(db.String(10000))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # bookings = db.relationship('Booking', back_populates='user')
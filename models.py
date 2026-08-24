from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


db = SQLAlchemy()

# Association table for User ↔ Club
participation = db.Table('participation',
    db.Column('user_id', db.Integer,
              db.ForeignKey('user.id'),
              primary_key=True),

    db.Column('event_id', db.Integer,
              db.ForeignKey('event.id'),
              primary_key=True)
)


user_club = db.Table(
    'user_club',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    profile_picture = db.Column(db.String(200), default='default_avatar.png')
    is_admin = db.Column(db.Boolean, default=False)
    events = db.relationship('Event', secondary=participation, backref=db.backref('participants', lazy='dynamic'))
    clubs = db.relationship('Club', secondary=user_club, backref='members')


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    # 🔥 VERY IMPORTANT
    events = db.relationship('Event', backref='club', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)

    event_date = db.Column(db.String(50))
    reg_start = db.Column(db.String(50))
    reg_end = db.Column(db.String(50))

    location = db.Column(db.String(100))
    poster = db.Column(db.String(200))
    form_link = db.Column(db.String(300))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    capacity = db.Column(db.Integer, default=50)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(100))  # image filename
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


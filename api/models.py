#!/usr/bin/python3

"""
"""
from api import db, login_manager
from datetime import datetime
from api import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """ """
    return User.query.get(int(user_id))

class Breeding_Rabbit(db.Model):
    """class that defines the fields to store breed rabbit info in the database 
    """
    id = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    breed = db.Column(db.String(30), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    owner_breed = db.Column(db.Integer(), db.ForeignKey('user.id'))


class Meat_Rabbit(db.Model):
    """class that defines the fields to store breed rabbit info in the database
    """
    id = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    owner_meat = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        """string representation of objects"""
        return ("Meat_Rabbit {} is {}".format(self.id, self.title))


class User(db.Model, UserMixin):
    """class that defines the fields to store users in the database """
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(60), nullable=False)
    breed_rabbit_items = db.relationship('Breeding_Rabbit', backref='breed_owned_user', lazy=True)
    meat_rabbit_items = db.relationship('Meat_Rabbit', backref='meat_owned_user', lazy=True)


    def __repr__(self):
        """string representation of objects"""
        return ("User {} is {}".format(self.id, self.firstname))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
class Photo(db.Model):
    """ """
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(70), nullable=False)
    data = db.Column(db.LargeBinary)

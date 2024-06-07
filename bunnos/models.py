#!/usr/bin/python3

"""
"""
from datetime import datetime
from flask_login import UserMixin

from . import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    """ """
    return User.query.get(int(user_id))


class Breeding_Rabbit(db.Model):
    """class that defines the fields to store breed rabbit info in the database"""

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
    filename = db.Column(db.String(70), nullable=False)
    data = db.Column(db.String)
    owner_breed = db.Column(db.Integer(), db.ForeignKey("user.id"))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_phone = db.Column(db.String(14), nullable=False)
    owner_firstname = db.Column(db.String(30), nullable=False)
    owner_lastname = db.Column(db.String(30), nullable=False)
    advert_id = db.Column(db.String(70), nullable=False)

    @property
    def pretty_price(self):
        """ """
        if len(str(self.price)) >= 4:
            return f"{str(self.price)[:-3]},{str(self.price)[-3:]}"
        else:
            return f"{self.price}"


class Meat_Rabbit(db.Model):
    """class that defines the fields to store breed rabbit info in the database"""

    id = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    filename = db.Column(db.String(70), nullable=False)
    data = db.Column(db.String)
    owner_meat = db.Column(db.Integer(), db.ForeignKey("user.id"))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_phone = db.Column(db.String(14), nullable=False)
    owner_firstname = db.Column(db.String(30), nullable=False)
    owner_lastname = db.Column(db.String(30), nullable=False)
    advert_id = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        """string representation of objects"""
        return "Meat_Rabbit {} is {}".format(self.id, self.title)

    @property
    def pretty2_price(self):
        """ """
        if len(str(self.price)) >= 4:
            return f"{str(self.price)[:-3]},{str(self.price)[-3:]}"
        else:
            return f"{self.price}"


class User(db.Model, UserMixin):
    """class that defines the fields to store users in the database"""

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(60), nullable=False)
    breed_rabbit_items = db.relationship(
        "Breeding_Rabbit", backref="breed_owner", lazy=True
    )
    meat_rabbit_items = db.relationship("Meat_Rabbit", backref="meat_owner", lazy=True)

    def __repr__(self):
        """string representation of objects"""
        return "User {} is {}".format(self.id, self.firstname)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Escrow_buyer(db.Model):
    """ """

    id = db.Column(db.Integer(), primary_key=True)
    advert_id = db.Column(db.String(70), nullable=False)
    price_agreed = db.Column(db.String(10), nullable=False)
    proof_of_payment = db.Column(db.String(70), nullable=False)
    buyer_firstname = db.Column(db.String(30), nullable=False)
    buyer_lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)


class Escrow_seller(db.Model):
    """ """

    id = db.Column(db.Integer(), primary_key=True)
    advert_id = db.Column(db.String(70), nullable=False)
    price_agreed = db.Column(db.String(10), nullable=False)
    filename = db.Column(db.String(70), nullable=False)
    data = db.Column(db.String)
    seller_firstname = db.Column(db.String(30), nullable=False)
    seller_lastname = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """string representation of objects"""
        return "Ad id is {} and price agreed is  {}".format(
            self.advert_id, self.price_agreed
        )

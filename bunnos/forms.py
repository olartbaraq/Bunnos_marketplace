#!/bin/usr/python3
"""
neccessary modules and packages imported for functions to run
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, DataRequired, ValidationError
from bunnos.models import User


class RegisterForm(FlaskForm):
    """This creates a form to be stored in the database as a sign-up form details for users """

    # This function checks if the unique field email in the register form
    # to be filled by the user in the sign-up page of the website has
    # already stored an existing email address in the database

    def validate_email(self, email_to_check):
        """checks if email already existed """
        user_email = User.query.filter_by(email=email_to_check.data).first()
        if user_email:
            raise ValidationError('Email already exists!')


    # This function checks if the unique field phone number in the register form
    # to be filled by the user in the sign-up page of the website has
    # already stored an existing phone ni=umber in the database

    def validate_phone(self, phone_to_check):
        """checks if phone is already existed """
        user_phone = User.query.filter_by(phone=phone_to_check.data).first()
        if user_phone:
            raise ValidationError('Phone Number already exists!')

    
    lastname = StringField(label="Lastname", validators=[Length(min=2, max=30), DataRequired()])
    firstname = StringField(label="Firstname", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email", validators=[Length(min=2, max=50), DataRequired()])
    phone = StringField(label="Phone", validators=[Length(min=11, max=14), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=8, max=60), DataRequired()])
    register = SubmitField(label="Register")


    
class PostAdForm(FlaskForm):
    """ """
    state = StringField(label="State", validators=[DataRequired()])
    title = StringField(label="Title", validators=[DataRequired()])
    quantity = IntegerField(label="Quantity", validators=[DataRequired()])
    category = StringField(label="Category", validators=[DataRequired()])
    price = StringField(label="Price", validators=[DataRequired()])
    weight = StringField(label="Weight", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    post_ad = SubmitField(label="POST AD")

    

class SignInForm(FlaskForm):
    """ """
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    Login = SubmitField(label="Sign In")


class PostAdForm2(FlaskForm):
    """ """
    state = StringField(label="State", validators=[DataRequired()])
    title = StringField(label="Title", validators=[DataRequired()])
    breed = StringField(label="Breed", validators=[DataRequired()])
    color = StringField(label="Color", validators=[DataRequired()])
    age = StringField(label="Age", validators=[DataRequired()])
    category = StringField(label="Category", validators=[DataRequired()])
    price = StringField(label="Price", validators=[DataRequired()])
    weight = StringField(label="Weight", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    post_ad = SubmitField(label="POST AD")


class SearchForm(FlaskForm):
    """ """
    searched = StringField(label="searched")
    Search = SubmitField(label="Search")
    

class BuyerEscrowForm(FlaskForm):
    """ """
    advert_id = StringField(label="Ad id", validators=[DataRequired()])
    price_agreed = StringField(label="Price", validators=[DataRequired()])
    bank_trans_ref = StringField(label="trans-ref", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class SellerEscrowForm(FlaskForm):
    """ """
    advert_id = StringField(label="Ad id", validators=[DataRequired()])
    price_agreed = StringField(label="Price", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


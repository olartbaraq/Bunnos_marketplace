#!/bin/usr/python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, DataRequired, ValidationError
from api.models import User


class RegisterForm(FlaskForm):
    """ """
    def validate_email(self, email_to_check):
        """ """
        user_email = User.query.filter_by(email=email_to_check.data).first()
        if user_email:
            raise ValidationError('Email already exists!')

    def validate_phone(self, phone_to_check):
        """ """
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
    state = StringField(label="State")
    title = StringField(label="Title")
    quantity = IntegerField(label="Quantity")
    category = StringField(label="Category")
    price = StringField(label="Price")
    weight = IntegerField(label="Weight")
    description = TextAreaField(label="Description")
    post_ad = SubmitField(label="POST AD")


class UploadForm(FlaskForm):
    """ """
    filename = FileField(label="filename", validators=[FileRequired()])
    submit = SubmitField(label="submit")



class SignInForm(FlaskForm):
    """ """
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    Login = SubmitField(label="Sign In")

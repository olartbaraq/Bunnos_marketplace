#!/usr/bin/python3

"""

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bunnosmarketplace.db'
app.config['SECRET_KEY'] = '011c6d0ce1fe9bd0b2fc7c89'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "sign_in"
login_manager.login_message_category = 'info'


from api import routes

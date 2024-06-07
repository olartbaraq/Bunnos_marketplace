#!/usr/bin/python3

"""
Some important modules are to be imported to make the flask-sqlalchemy work
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///bunnoswebsite.db"  # Replace with your actual database URI
    )
    app.config["SECRET_KEY"] = "011c6d0ce1fe9bd0b2fc7c89"

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "sign_in"
    login_manager.login_message_category = "info"

    from .routes import bp  # Import the blueprint

    app.register_blueprint(bp)  # Register the blueprint

    return app


# # this creates an instance of the Flask module imported from flask package
# app = Flask(__name__)

# # this set the database used to the in-built sqlite3
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bunnoswebsite.db"

# # this is necessary to be set in order for wtforms
# # with http methods to function
# app.config["SECRET_KEY"] = "011c6d0ce1fe9bd0b2fc7c89"

# # this set the instance app to make use of sqlalchemy
# # as an ORM to store data to sqlite3 database
# db = SQLAlchemy(app)

# # this helps hash the password inputted to the form
# # not to be stored as a plain text in the database
# bcrypt = Bcrypt(app)

# # this set the app instance as an instance of LoginManager
# # for a user to sign-in the website using their credentials
# # that has been stored on the database
# login_manager = LoginManager(app)

# login_manager.login_view = "sign_in"

# # this set the flash message to display the key:value
# # pairs of information regarding sign-in of a user
# login_manager.login_message_category = "info"

# with app.app_context():
#     db.drop_all()
#     db.create_all()


# # this makes it easy to prevent circular imports of modules from
# # routes.py file to access the above instances and variables

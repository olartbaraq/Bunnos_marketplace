#!/usr/bin/python3

"""
Starts a Flash web Application for a rabbit marketplace

"""
from api import app
from flask import render_template, url_for, redirect, request, flash
from api.models import User, Meat_Rabbit, Breeding_Rabbit #Photo
from api.forms import RegisterForm, PostAdForm, SignInForm #UploadForm
from api import db
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home_page():
    """a route to return the website homepage"""
    return render_template('home.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    """a route to return the website sign in page"""
    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email.data).first()
            if attempted_user and attempted_user.check_password_correction(
                    attempted_password=form.password.data):
                login_user(attempted_user)
                flash("Welcome; You are logged in as {} {}".
                      format(attempted_user.firstname,
                             attempted_user.lastname), category='success')
                return redirect(url_for('home_page'))
            else:
                flash("Email address and password are not match! Please try again", category='danger')
    return render_template('sign_in.html', form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """a route to return the website sign up page"""
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = User(email=form.email.data,
                                  lastname=form.lastname.data,
                                  firstname=form.firstname.data,
                                  phone=form.phone.data,
                                  password=form.password.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    return render_template('sign_up.html', form=form)

@app.route('/sell/breeding_rabbit')
def breeding_rabbit():
    """a route to return the website sign up page"""
    return render_template('breeding-rabbit.html')

@app.route('/sell/meat_rabbit', methods=['GET', 'POST'])
def meat_rabbit():
    """a route to return the website sign up page"""
    form = PostAdForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            meat_rabbit_to_create = Meat_Rabbit(title=form.title.data,
                                                state=form.state.data,
                                                quantity=form.quantity.data,
                                                category=form.category.data,
                                                price=form.price.data,
                                                weight=form.weight.data,
                                                description=form.description.data)
            db.session.add(meat_rabbit_to_create)
            db.session.commit()
            return redirect(url_for('home_page'))
    return render_template('meat-rabbit.html', form=form)


@app.route('/sell/upload_photo')
def upload_photo():
    """ """
    return render_template('meat-upload.html')

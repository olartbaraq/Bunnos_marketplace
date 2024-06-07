#!/usr/bin/python3

"""
Starts a Flash web Application for a rabbit marketplace

"""
from flask import render_template, url_for, redirect, request, flash
from bunnos.models import (
    User,
    Meat_Rabbit,
    Breeding_Rabbit,
    Escrow_buyer,
    Escrow_seller,
)
from bunnos.forms import (
    RegisterForm,
    PostAdForm,
    SignInForm,
    PostAdForm2,
    SearchForm,
    BuyerEscrowForm,
    SellerEscrowForm,
)
from flask import Blueprint
from bunnos import db
from flask_login import login_user, logout_user, login_required, current_user
import base64
import uuid

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/home")
def home_page():
    """a route to return the website homepage"""
    breed_posts = Breeding_Rabbit.query.order_by(
        Breeding_Rabbit.date_created.desc()
    ).limit(10)
    meat_posts = Meat_Rabbit.query.order_by(Meat_Rabbit.date_created.desc()).limit(10)
    return render_template("home.html", breed_posts=breed_posts, meat_posts=meat_posts)


@bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    """a route to return the website sign in page"""
    form = SignInForm()
    if request.method == "POST":
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email.data).first()
            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(
                    "Welcome; You are logged in as {} {}".format(
                        attempted_user.firstname, attempted_user.lastname
                    ),
                    category="success",
                )
                return redirect(url_for("main.home_page"))
            else:
                flash(
                    "Email address and password are not match! Please try again",
                    category="danger",
                )
    return render_template("sign_in.html", form=form)


@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """a route to return the website sign up page"""
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_create = User(
                email=form.email.data,
                lastname=form.lastname.data,
                firstname=form.firstname.data,
                phone=form.phone.data,
                password=form.password.data,
            )
            db.session.add(user_to_create)
            db.session.commit()
            flash("Registration Sucessful, you can login now", category="info")
            return redirect(url_for("main.home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category="danger")
    return render_template("sign_up.html", form=form)


@bp.route("/sell/breeding_rabbit", methods=["GET", "POST"])
@login_required
def breeding_rabbit():
    """a route to return the website sign up page"""
    form = PostAdForm2()
    if request.method == "POST":
        if form.validate_on_submit():
            file = request.files["file"]
            blob_file = file.read()
            file_string = base64.b64encode(blob_file).decode("utf-8")
            breeding_rabbit_to_create = Breeding_Rabbit(
                title=form.title.data,
                state=form.state.data,
                breed=form.breed.data,
                color=form.color.data,
                age=form.age.data,
                category=form.category.data,
                price=form.price.data,
                weight=form.weight.data,
                description=form.description.data,
                filename=file.filename,
                data=file_string,
                owner_breed=current_user.id,
                owner_phone=current_user.phone,
                owner_firstname=current_user.firstname,
                owner_lastname=current_user.lastname,
                advert_id=uuid.uuid4().hex,
            )
            db.session.add(breeding_rabbit_to_create)
            db.session.commit()
            flash(
                "Your ad is successfully created, it will be live in a few minutes",
                category="info",
            )
            # print(file_string)
            return redirect(url_for("main.home_page"))
    return render_template("breeding-rabbit.html", form=form)


@bp.route("/sell/meat_rabbit", methods=["GET", "POST"])
@login_required
def meat_rabbit():
    """a route to return the website sign up page"""
    form = PostAdForm()
    if request.method == "POST":
        if form.validate_on_submit():
            file = request.files["file"]
            blob_file = file.read()
            file_string = base64.b64encode(blob_file).decode("utf-8")
            meat_rabbit_to_create = Meat_Rabbit(
                title=form.title.data,
                state=form.state.data,
                quantity=form.quantity.data,
                category=form.category.data,
                price=form.price.data,
                weight=form.weight.data,
                description=form.description.data,
                filename=file.filename,
                data=file_string,
                owner_meat=current_user.id,
                owner_phone=current_user.phone,
                owner_firstname=current_user.firstname,
                owner_lastname=current_user.lastname,
                advert_id=uuid.uuid4().hex,
            )
            db.session.add(meat_rabbit_to_create)
            db.session.commit()
            flash(
                "Your ad is successfully created, it will be live in a few minutes",
                category="info",
            )
            return redirect(url_for("main.home_page"))
    return render_template("meat-rabbit.html", form=form)


@bp.route("/logout")
def logout():
    """ """
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("main.home_page"))


@bp.route("/profile/saved")
@login_required
def profile_page():
    """ """
    if current_user in User.query.all():
        parent_list = current_user.breed_rabbit_items
        parent_meat = current_user.meat_rabbit_items

    return render_template(
        "profile.html", parent_list=parent_list, parent_meat=parent_meat
    )


@bp.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@bp.route("/search", methods=["POST", "GET"])
def search():
    form = SearchForm()
    ad_breed = Breeding_Rabbit.query
    ad_meat = Meat_Rabbit.query
    if request.method == "POST":
        if form.validate_on_submit():
            ad_search = form.searched.data
            ad_breed = ad_breed.filter(
                Breeding_Rabbit.description.like("%" + ad_search + "%")
            )
            ad_meat = ad_meat.filter(
                Meat_Rabbit.description.like("%" + ad_search + "%")
            )
            ad_breed = ad_breed.order_by(Breeding_Rabbit.title).all()
            ad_meat = ad_meat.order_by(Meat_Rabbit.title).all()
            return render_template(
                "search.html",
                form=form,
                searched=ad_search,
                ad_breed=ad_breed,
                ad_meat=ad_meat,
            )


@bp.route("/ad_posts_breed", methods=["POST", "GET"])
def breed_posts_page():
    """ """
    breed_posts = Breeding_Rabbit.query.order_by(Breeding_Rabbit.date_created)
    return render_template("breed_posts.html", breed_posts=breed_posts)


@bp.route("/ad_posts_meat", methods=["POST", "GET"])
def meat_posts_page():
    """ """
    meat_posts = Meat_Rabbit.query.order_by(Meat_Rabbit.date_created)
    return render_template("meat_posts.html", meat_posts=meat_posts)


@bp.route("/ad_posts/breed/<int:id>")
def breed_post(id):
    """ """
    breed_post = Breeding_Rabbit.query.get_or_404(id)
    return render_template("ind_breed_post.html", breed_post=breed_post)


@bp.route("/ad_posts/meat/<int:id>")
def meat_post(id):
    """ """
    meat_post = Meat_Rabbit.query.get_or_404(id)
    return render_template("ind_meat_post.html", meat_post=meat_post)


@bp.route("/escrow")
@login_required
def escrow_page():
    """ """
    return render_template("escrow.html")


@bp.route("/escrow/buyer", methods=["POST", "GET"])
@login_required
def escrow_buyer():
    """ """
    buyer_info = Escrow_buyer.query.filter_by(email=current_user.email).all()
    form = BuyerEscrowForm()
    if request.method == "POST":
        if form.validate_on_submit():
            trade_to_create = Escrow_buyer(
                advert_id=form.advert_id.data,
                price_agreed=form.price_agreed.data,
                proof_of_payment=form.bank_trans_ref.data,
                buyer_firstname=current_user.firstname,
                buyer_lastname=current_user.lastname,
                email=current_user.email,
            )
            db.session.add(trade_to_create)
            db.session.commit()
            flash("Data received sucessfully", category="info")
            return redirect(url_for("main.escrow_page"))
    return render_template("escrow-buyer.html", form=form, buyer_info=buyer_info)


@bp.route("/escrow/seller", methods=["POST", "GET"])
@login_required
def escrow_seller():
    """ """
    form = SellerEscrowForm()
    if request.method == "POST":
        if form.validate_on_submit():
            file = request.files["file"]
            blob_file = file.read()
            file_string = base64.b64encode(blob_file).decode("utf-8")
            trade_to_create = Escrow_seller(
                advert_id=form.advert_id.data,
                price_agreed=form.price_agreed.data,
                filename=file.filename,
                data=file_string,
                seller_firstname=current_user.firstname,
                seller_lastname=current_user.lastname,
            )
            db.session.add(trade_to_create)
            db.session.commit()
            flash("Data received sucessfully", category="info")
            return redirect(url_for("main.escrow_page"))
    return render_template("escrow-seller.html", form=form)


@bp.route("/escrow/delivery<int:id>", methods=["GET", "DELETE"])
@login_required
def delivery(id):
    """ """
    order_to_delete = Escrow_buyer.query.get_or_404(id)
    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        flash("Funds sent to Seller successfully", category="info")
        buyer_info = Escrow_buyer.query.filter_by(email=current_user.email).all()
        return render_template("escrow.html", buyer_info=buyer_info)
    except:
        flash("whoops")
        buyer_info = Escrow_buyer.query.filter_by(email=current_user.email).all()
        return render_template("escrow.html", buyer_info=buyer_info)

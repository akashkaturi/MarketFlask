
from market import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        print('hi')
        purchased_item = request.form.get('purchased_item')
        purchased_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_object:
            if current_user.can_purchase(purchased_object.price):
                purchased_object.buy(current_user)
                flash(
                    f'Congratulations {current_user.user_name.title()} you have purchased {purchased_object.name} for ${purchased_object.price}.', category='success')
            else:
                flash(
                    f"Sorry you don't have enough money to buy {purchased_item}, your current funds are {current_user.budget}", category='danger')

        sold_item = request.form.get('sold_item')
        sold_object = Item.query.filter_by(name=sold_item).first()
        if sold_object:
            if current_user.can_sell(sold_object):
                sold_object.sell(current_user)
                flash(
                    f'The item {sold_object.name} is sold to the market for ${sold_object.price}',category='success')
            else:
                flash(f'Something wrong with selling the {sold_object.name}')
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, sell_form=sell_form, owned_list=owned_items)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            user_name=form.username.data,
            email_address=form.email.data,
            password=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'The error occured is: {err[0]}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            user_name=form.user_name.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'You are successfully logged in as {attempted_user.user_name}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('User name and password didnot match, please try again',
                  category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You are successfully logged out. ', category='info')
    return redirect(url_for('home_page'))

from enum import unique
from market import db
from market import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    user_name = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50),
                              unique=True, nullable=False)
    password_hash = db.Column(db.String(length=65), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=1000000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_test_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_test_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    @property
    def pretty_budget(self):
        return f'{self.budget:,}'

    def can_purchase(self, item_price):
        return self.budget >= item_price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # owned_user = db.relationship('User', backref='items', lazy=True)

    def __repr__(self):
        return f'Item: {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
        
    def sell(self,user):
        self.owner=None
        user.budget+=self.price
        db.session.commit()

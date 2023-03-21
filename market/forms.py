from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(user_name=username_to_check.data).first()
        if user:
            raise ValidationError(
                "The user already exists choose another user name")

    def validate_email(self, email_to_Check):
        email = User.query.filter_by(email_address=email_to_Check.data).first()
        if email:
            raise ValidationError(
                "The email already exists, Please try a different mail")

    username = StringField(label='User Name:', validators=[
        Length(min=3, max=30), DataRequired()])
    email = StringField(label='email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password:', validators=[
        Length(min=6), DataRequired()])
    password2 = PasswordField(label='confirm password:', validators=[
        EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    user_name = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')

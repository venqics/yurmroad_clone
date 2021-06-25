from flask_wtf import FlaskForm
from wtforms.validators import Length, Email, required, EqualTo, URL, Optional
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.html5 import DecimalField
from yumroad.models import User

class EmptyForm(FlaskForm):
    pass

class ProductForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=60)])
    description = StringField('Description')
    picture_url = StringField('Picture URL', description='Optional', validators=[validators.Optional(), validators.URL()])
    price = DecimalField('Price', description='in USD, Optional')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.email(), validators.required()])
    password = PasswordField('Password', validators=[validators.required()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Invalid email or password')
            return False

        if not check_password_hash(user.password, self.password.data):
            self.email.errors.append('Invalid email or password')
            return False
        return True

class SignupForm(FlaskForm):
    store_name = StringField('Store Name', validators=[validators.required(), validators.length(min=4)])
    email = StringField('Email', validators=[validators.email(), validators.required()])
    password = PasswordField('Password', validators=[validators.required(), validators.length(min=4),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[validators.required()])

    def validate(self):
        check_validate = super(SignupForm, self).validate()
        if not check_validate:
            return False

        # Does the user exist already? Must return false,
        # otherwise we'll allow anyone to sign in
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('That email already has an account')
            return False
        return True

        # TODO: Maybe you'll want a validation to prevent the same store name from being used twice


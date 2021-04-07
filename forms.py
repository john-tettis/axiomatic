from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional


class SignupForm(FlaskForm):
    """User signup form"""

    username = StringField('Username',[DataRequired()])

    email = StringField('Email',[DataRequired(), Email()])

    password = PasswordField('Password',[DataRequired()])

    image_url = StringField('Image URL', [URL(), Optional()])

class LoginForm(FlaskForm):
    """User login form"""

    username = StringField('Username',[DataRequired()])

    password = PasswordField('Password',[DataRequired()])
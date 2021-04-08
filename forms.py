from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional


class SignupForm(FlaskForm):
    """User signup form"""

    username = StringField('Username',[DataRequired('Please enter a username.'), Length(max=30)])

    email = StringField('Email',[DataRequired('Please enter an email.'), Email('Please choose a valid email address.')])

    password = PasswordField('Password',[DataRequired('Please enter a password.')])

    image_url = StringField('Image URL', [URL('Must be a valid url.'), Optional()])

class LoginForm(FlaskForm):
    """User login form"""

    username = StringField('Username',[DataRequired('Username is required')])

    password = PasswordField('Password',[DataRequired('Password is required.')])

class EditAccountForm(FlaskForm):
    username = StringField('Username',[DataRequired('Username cannot be empty')])

    email = StringField('Email',[DataRequired('Email cannot be empty.'), Email('Please choose a valid email.')])
    
    bio = TextAreaField('Bio', [Length(max=200)])

    image_url = StringField('Image URL', [URL('Must be a valid url.'), Optional()])


class QuoteForm(FlaskForm):

    content = TextAreaField('Your wise words:', [DataRequired('You gotta say something!'), Length(max=300, message="Quote is over 300 characters - keep it concise!")])

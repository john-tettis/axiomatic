from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Poet
from forms import SignupForm, LoginForm



app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///dont-quote-me'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "it's a secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
toolbar = DebugToolbarExtension(app)

CURR_POET = 'current_poet'
connect_db(app)
db.create_all()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///dont-quote-me'



@app.before_request
def add_user_to_g():
    """Login poet to global variable"""

    if CURR_POET in session:
        g.poet = Poet.query.get(session[CURR_POET])

    else:
        g.poet = None


def do_login(poet):
    """Log in poet."""

    session[CURR_POET] = poet.username


def do_logout():
    """Logout poet."""

    if CURR_POET in session:
        del session[CURR_POET]

@app.route('/')
def show_homepage():
    if g.poet:
        return render_template('home.html')
    else:
        return render_template('home_anon.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    form = SignupForm()

    if form.validate_on_submit():
        try:
            poet = Poet.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or Poet.image_url.default.arg)
            db.session.commit()
            do_login(poet)
            return redirect('/')
        except IntegrityError:
            beans = IntegrityError
            raise
            return redirect('/beans')
    return render_template('/user/signup.html', form = form)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        poet = Poet.authenticate(username,password)
        if poet:
            do_login(poet)
            return redirect('/')
        
    return render_template('/user/login.html', form = form)

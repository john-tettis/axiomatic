from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Poet, Quote
from forms import SignupForm, LoginForm, EditAccountForm, QuoteForm
from request import retrieve_quotes



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
        g.poet = Poet.query.filter_by(username = session[CURR_POET]).first()

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


# user routes
# ************************************************************************************
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
    if g.poet:
        flash("you are already logged in!")
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        poet = Poet.authenticate(username,password)
        if poet:
            do_login(poet)
            return redirect('/')
        else:
            form.username.errors.append('Invalid username or password')
        
    return render_template('/user/login.html', form = form)
@app.route('/logout')
def logout():
    do_logout()
    flash('Logged out')
    return redirect('/')

@app.route('/account')
def account_info():
    if not g.poet:
        raise
        flash('You must login to access this page!')
        return redirect('/')
    else:
        return render_template('/user/information.html')
    
@app.route('/account/edit', methods = ['GET','POST'])
def account_edit():
    if not g.poet:
        flash('You must login to access this page!')
        return redirect('/')
    else:
        form = EditAccountForm(obj = g.poet)

        if form.validate_on_submit():
            poet = Poet.query.filter_by(username=g.poet.username).first()
            try:
                poet.username = form.username.data
                poet.email = form.email.data
                poet.bio = form.bio.data
                poet.image_url = form.image_url.data
                db.session.add(poet)
                db.session.commit()
                do_login(poet)
                return redirect('/account')
            except IntegrityError:
                flash('Oops, something went wrong...')
                return redirect('/')
        return render_template('/user/edit.html', form= form)
    
# Quote routes
# **************************************************************************************************

@app.route('/quotes')
def display_quotes():
    filt= request.args.get('f','famous')
    quotes = retrieve_quotes(filt)
    return render_template('/quotes/quotes.html', quotes = quotes)

@app.route('/quotes/new', methods=['GET','POST'])
def new_quotes():

    form = QuoteForm()

    if form.validate_on_submit():
        quote = Quote(content = form.content.data, poet_id = g.poet.id)
        db.session.add(quote)
        db.session.commit()
        return redirect(f'/quotes/{quote.id}')
    else:
        return render_template('quotes/new.html', form=form)

@app.route('/quotes/<int:id>')
def display_quote(id):
    quote = Quote.query.get_or_404(id)
    return render_template('quotes/info.html', quote = quote)


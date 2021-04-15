from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Poet, Quote, Share, Comment, follows
from forms import SignupForm, LoginForm, EditAccountForm, QuoteForm
from request import retrieve_quotes, add_fam_like, add_poet_like, repost_fam, repost_user, get_user_quotes, get_qod



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
app.debug = False
app.config['DEBUG'] = False
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
        quote = get_qod()
        return render_template('home.html',quote=quote)
    else:
        return render_template('home_anon.html')\

@app.route('/about')
def show_about_page():
    """Display the information about this project"""
    return render_template('about.html')


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
        flash('You must login to access this page!')
        return redirect('/')
    else:
        filt = request.args.get('f','own')
        quotes = get_user_quotes(filt=filt,poet=g.poet)
        return render_template('/user/information.html', quotes=quotes)
    
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

@app.route('/poets/<int:id>')
def poet_info(id):
    """Displays poet info associated with another account"""
    poet = Poet.query.get_or_404(id)
    if poet == g.poet:
        return redirect('/account')
    filt = request.args.get('f','own')
    quotes = get_user_quotes(filt=filt,poet=poet)
    return render_template('/user/information_anon.html',poet=poet, quotes=quotes)

@app.route('/follow', methods=['POST'])
def follow():
    poet_id = request.form.get('poet')
    poet = Poet.query.get_or_404(poet_id)
    poet.followers.append(g.poet)
    db.session.commit()
    return redirect(f'/poets/{poet_id}')

@app.route('/unfollow', methods=['POST'])
def unfollow():
    poet_id = request.form.get('poet')
    poet = Poet.query.get_or_404(poet_id)
    poet.followers.remove(g.poet)
    db.session.commit()
    return redirect(f'/poets/{poet_id}')


# Quote routes
# **************************************************************************************************

@app.route('/quotes')
def display_quotes():
    filt= request.args.get('f','famous')
    if filt == 'following':
        if not g.poet:
            flash('You are not logged in!')
            return redirect('/quotes')
    quotes = retrieve_quotes(filt)
    return render_template('/quotes/quotes.html', quotes = quotes)

@app.route('/quotes/new', methods=['GET','POST'])
def new_quotes():
    if not g.poet:
        flash('you must be logged in to create a quote!')
        return redirect('/')

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




# API routes
# ***********************************************


@app.route('/quotes/like', methods=['POST'])
def like_quote():
    """Add a like to a quote through an api route"""
    if not g.poet:
        return ({'message':'Not logged in'})
    content = request.json.get('content')
    author = request.json.get('author')
    quote_id = request.json.get('id')
    poet = g.poet
    if content:
        add_fam_like(content,author,poet)
    else:
        add_poet_like(quote_id,poet)

    return {'message':'Success.'}

@app.route('/quotes/like',methods=['DELETE'])
def remove_like():
    """Delete a poet-quote like relationship"""
    content = request.json.get('content')
    quote_id = request.json.get('id')
    poet = g.poet
    if content:
        quote = Quote.query.filter_by(content=content).first()
    elif id:
        quote = Quote.query.get(id)
    try:
        Like.query.filter_by(quote_id=quote.id,poet_id=g.poet.id).delete()
        db.session.commit()
        return {'success':'Like removed.'}
    except:
        db.session.rollback()
        return{'failed':'something went wrong'}


@app.route('/quotes/share',methods=['POST'])
def share_quote():
    """Respost a quote"""
    if not g.poet:
        return ({'message':'Not logged in'})
    content = request.json.get('content')
    author = request.json.get('author')
    quote_id = request.json.get('id')
    poet = g.poet
    if content:
        repost_fam(content=content, author=author,poet=poet)
    else:
        repost_user(quote_id=quote_id, poet_id=poet.id)

    return {'message':'Success'}

@app.route('/quotes/share',methods=['DELETE'])
def remove_share():
    """Delete a poet-quote share relationship"""
    content = request.json.get('content')
    quote_id = request.json.get('id')
    poet = g.poet
    import pdb 
    pdb.set_trace()
    if content:
        quote = Quote.query.filter_by(content=content).first()
    elif id:
        quote = Quote.query.get(quote_id)
   
    Share.query.filter_by(quote_id=quote.id,poet_id=g.poet.id).delete()
    db.session.commit()
    return {'success':'Like removed.'}
    # except:
    #     db.session.rollback()
    #     return{'failed':'something went wrong'}


@app.route('/comments/add', methods=["POST"])
def add_comment():
    if not g.poet:
        return ({'message':'Not logged in'})
    content = request.json.get('content')
    author = request.json.get('author')
    quote_content=request.json.get('quote_content')
    poet = g.poet
    quote = Quote.handle_api_quote(content=quote_content, author = author)

    comment = Comment(quote_id=quote.id, poet_id=poet.id,content=content)

    
    db.session.add(comment)
    db.session.commit()
    return {'message':quote_content}
    # except:
    #     db.session.rollback()
    #     return{'failed':'something went wrong'}








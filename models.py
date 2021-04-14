"""SQLAlchemy models."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


follows = db.Table('follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('poets.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('poets.id'), primary_key=True)
)

class Poet(db.Model):
    """User (poet) object"""
    __tablename__ ='poets'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30), unique=True)
    
    email = db.Column(db.String, unique=True, nullable=False)

    hashed_password = db.Column(db.String, nullable=False)

    image_url = db.Column(db.String, default='https://secure.gravatar.com/avatar/f25866817ff07876c8cedc80c4dbb979?s=150&r=g&d=https://chicagodispatcher.com/wp-content/plugins/userswp/assets/images/no_profile.png')

    bio = db.Column(db.String(200), nullable = True)

    followers = db.relationship('Poet', secondary=follows,
     primaryjoin= id == follows.c.follower_id,
     secondaryjoin=id == follows.c.followed_id,
     backref='following'
     )

    likes = db.relationship('Quote', secondary ='likes', lazy='subquery')

    comments = db.relationship('Comment')

    shares = db.relationship('Quote', secondary ='shares')

    quotes = db.relationship('Quote', backref = 'poet')

    @classmethod
    def signup(cls,username,password,email,image_url):
        """Hashes the password and creates a new poet account"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        poet = Poet(username=username,
                    hashed_password=hashed_pwd,
                    email=email,
                    image_url=image_url)

        db.session.add(poet)
        return poet
    
    @classmethod
    def authenticate(cls,username,password):
        """Authenticate a login attempt"""
        poet= cls.query.filter_by(username=username).first()

        if poet:
            is_auth = bcrypt.check_password_hash(poet.hashed_password, password)
            if is_auth:
                return poet

        return False


class Quote(db.Model):
    """User-made quotes."""
    __tablename__ ='quotes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=True)

    content = db.Column(db.String(200), nullable=False, unique=True)

    author = db.Column(db.String(80), nullable = True)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    likes = db.relationship('Like')

    comments = db.relationship('Comment', order_by='Comment.timestamp')

    @classmethod
    def handle_api_quote(cls, content, author):
        quote = cls.query.filter_by(content=content).first()

        if quote:
            return quote
        else:
            try:
                quote = Quote(content=content,author=author)
                db.session.add(quote)
                db.session.commit()
            except IntegrityError:
                quote = cls.query.filter_by(content=content).first()
            return quote


class Share(db.Model):
    __tablename__ ='shares'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    is_user_quote = db.Column(db.Boolean)

class Like(db.Model):
    __tablename__ ='likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))
    
    is_user_quote = db.Column(db.Boolean)


class Comment(db.Model):
    __tablename__ ='comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    content = db.Column(db.String(200), nullable=False)

    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    poet = db.relationship('Poet')


    

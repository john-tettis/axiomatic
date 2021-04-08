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


class Poet(db.Model):
    """User (poet) object"""
    __tablename__ ='poets'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30), unique=True)
    
    email = db.Column(db.String, unique=True, nullable=False)

    hashed_password = db.Column(db.String, nullable=False)

    image_url = db.Column(db.String, default='https://secure.gravatar.com/avatar/f25866817ff07876c8cedc80c4dbb979?s=150&r=g&d=https://chicagodispatcher.com/wp-content/plugins/userswp/assets/images/no_profile.png')

    bio = db.Column(db.String(200), nullable = True)

    likes = db.relationship('Like')

    comments = db.relationship('Comment')

    shares = db.relationship('Share')

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
        """Authenticaters a login attempt"""
        poet= cls.query.filter_by(username=username).first()

        if poet:
            is_auth = bcrypt.check_password_hash(poet.hashed_+password, password)
            if is_auth:
                return poet

        return False


class Quote(db.Model):
    """User-made quotes."""
    __tablename__ ='quotes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    content = db.Column(db.String(200), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    category = db.Column(db.String, nullable=True)

    likes = db.relationship('Like')


class TagCount(db.Model):
    __tablename__ ='tag_count'
    
    tag_name = db.Column(db.String,primary_key=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False, primary_key=True)

    count = db.Column(db.Integer, nullable=False)

class Share(db.Model):
    __tablename__ ='shares'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    user_quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))
    
    api_quote_id = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    is_user_quote = db.Column(db.Boolean)

class Like(db.Model):
    __tablename__ ='likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    user_quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))
    
    api_quote_id = db.Column(db.Text)

    is_user_quote = db.Column(db.Boolean)


class Comment(db.Model):
    __tablename__ ='comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    poet_id = db.Column(db.Integer, db.ForeignKey('poets.id', ondelete='cascade'), nullable=False)

    user_quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id', ondelete='cascade'))
    
    api_quote_id = db.Column(db.Text)

    is_user_quote = db.Column(db.Boolean)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


    

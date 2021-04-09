import requests
from models import Quote, Like, db, Share

url = "https://zenquotes.io/api/"

response = requests.request("GET", f'{url}/today')


def retrieve_quotes(filter):
    '''Retreive quotes from api or database depending on filter'''

    if filter == 'famous':
        return get_famous_quotes(50)
    if filter == 'community':
        return Quote.query.filter_by(author=None).order_by(Quote.timestamp).all()




def get_famous_quotes(limit):
    """Send request to api for 50 random quotes"""
    response = requests.request("GET", f'{url}/quotes')
    quotes = []

    for obj in response.json():

        quotes.append({
            'content': obj['q'],
            'author': obj['a']
        })
    return quotes

def get_user_quotes(filt, poet):
    """get likes, shares, or own quotes depending on filter passed"""
    if filt == 'own':
        return poet.quotes
    if filt == 'likes':
        return poet.likes
    if filt == 'shares':
        return poet.shares
    else:
        return poet.likes




def add_fam_like(content,author, poet):
    """Add a like to quote from the api - they do not have ids from the api so they must be stored in the database"""

    quote = Quote.handle_api_quote(content=content, author=author)

    like = Like(poet_id=poet.id, quote_id=quote.id, is_user_quote=False)
    db.session.add(like)
    db.session.commit()

def add_poet_like(quote_id,user):
    """Add a like to a user created quote"""

    like = Like(poet_id=poet.id, quote_id=quote_id, is_user_quote=True)
    db.session.add(like)
    db.session.commit()

def repost_fam(content,author,poet):
    """Repost an api quote"""
    quote = Quote.handle_api_quote(content=content,author=author)
    share = Share(poet_id=poet.id, quote_id=quote.id,is_user_quote=False)
    db.session.add(share)
    db.session.commit()

def repost_user(quote_id,poet_id):
    """Repost a user quote"""
    share = Share(poet_id=poet.id, quote_id=quote_id, is_user_quote=True)
    db.session.add(share)
    db.session.commit()
"""Message model tests."""

import os
from unittest import TestCase

from models import db, Poet, Quote, Comment

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///axiomatic-test"


# Now we can import app

from app import app
app.debug = False
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class PoetModelTestCase(TestCase):
    """Test the message model"""

    def setUp(self):
        """Clear data and give test info"""
        Poet.query.delete()

    def test_Quote_model(self):
        """Does the quote model work?"""

        poet = Poet.signup(username='test',password='test_password',email="test@test.com",image_url=None)
        db.session.add(poet)
        db.session.commit()

        quote = Quote(content='this is a test message',poet_id=poet.id)
        db.session.add(quote)
        db.session.commit()
        self.assertEqual(quote.poet,poet)
        self.assertEqual(quote.content,'this is a test message')
    def test_poet_model(self):
        """Does poet model work?"""

        poet = Poet.signup(username='test',password='test_password',email="test@test.com",image_url=None)
        db.session.add(poet)
        db.session.commit()
        self.assertEqual(poet.username, 'test')
        self.assertEqual(Poet.authenticate(username='test',password='test_password'),poet)
    
    def test_comment_model(self):
        """Does the comment functionality work?"""
        poet = Poet.signup(username='test',password='test_password',email="test@test.com",image_url=None)
        db.session.add(poet)
        db.session.commit()
        quote = Quote(content='this is a test message',poet_id=poet.id)
        db.session.add(quote)
        db.session.commit()
        comment = Comment(content='test comment', poet_id=poet.id,quote_id=quote.id)
        db.session.add(comment)
        db.session.commit()

        self.assertEqual(comment.poet,poet)
        self.assertEqual(comment.content,'test comment')
        self.assertIn(comment, quote.comments)

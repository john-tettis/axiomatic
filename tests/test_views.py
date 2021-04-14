"""Message model tests."""

import os
from unittest import TestCase

from models import db, Poet, Quote, Comment, Like
from app import app, session, do_login, g


app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///axiomatic-test'
CURR_POET = 'current_poet'

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

#  with c.session_transaction() as sess:
#                 sess[CURR_POET] = self.poet.id
class TestUserViews(TestCase):
    """Test the user signup, login, logout functions"""

    def setUp(self):
        """Create test client, add sample data."""

        Poet.query.delete()
        Quote.query.delete()

        self.client = app.test_client()

        self.poet = Poet.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_signup(self):
        """Does the signup route work"""
        with self.client as c:
            resp = c.post("/signup", data={
                "username": "test",
                "password":"test_password",
                "email":'test2@test.com'
                })

            self.assertEqual(resp.status_code, 302)

          
            self.assertTrue(Poet.authenticate(username='test',password='test_password') !=False)
    def test_login(self):
        """DOes the login route function properly"""
        with self.client as c:
            resp = c.post("/login", data={
                "username": "testuser",
                "password":"testuser"
                },follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Logout', resp.data)
            
    def test_logout(self):
        """Does the logout route work"""

        
        with self.client as c:
            c.post("/login", data={
                "username": "testuser",
                "password":"testuser"
                })
            resp = c.get("/logout",follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Logged out', resp.data)
            self.assertTrue(g.poet==None)


class TestQuoteRoutes(TestCase):
    """Do the quote routes function properly"""
    def setUp(self):
        """Create test client, add sample data."""

        Poet.query.delete()
        Quote.query.delete()

        self.client = app.test_client()

        self.poet = Poet.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()
        with self.client as c:
            c.post("/login", data={
                    "username": "testuser",
                    "password":"testuser"
                    })


    def test_new_quote(self):
        """Can a poet create a new quote"""

        with self.client as c:
            

            resp =  c.post('/quotes/new',data={
                'content':'Test quote',
                'poet_id':self.poet.id
            })
            self.assertEqual(resp.status_code,302)
            self.assertTrue(Quote.query.filter_by(content='Test quote').first()!=None)
    
    def test_like_quote(self):
        """Does the like functionality work"""
        
        with self.client as c:
            c.post('/quotes/new',data={
                'content':'Test quote',
                'poet_id':self.poet.id
            })
            quote = Quote.query.filter_by(content='Test quote').one()
            resp = c.post('/quotes/like', data={
                'quote_id': quote.id
            }, content_type='application/json')
            self.assertEqual(resp.status_code,400)
            self.assertTrue(Like.query.filter_by(quote_id=quote.id,poet_id=self.poet.id)!=None)
        
    def test_delete_quotes(self):
        """Does the delete functionality work"""
        with self.client as c:
            c.post('/quotes/new',data={
                'content':'Test quote',
                'poet_id':self.poet.id
            })
            quote = Quote.query.filter_by(content='Test quote').one()
            resp = c.delete('/quotes', data={
                'quote_id': quote.id
            }, content_type='application/json')
            self.assertEqual(resp.status_code,405)
            self.assertTrue(Like.query.filter_by(quote_id=quote.id,poet_id=self.poet.id)!=None)
    

class TestBasicRoutes(TestCase):
    """Do the basic navigation links function properly"""

    def setUp(self):
        """Create test client, add sample data."""

        Poet.query.delete()
        Quote.query.delete()

        self.client = app.test_client()

        self.poet = Poet.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()
        with self.client as c:
            c.post("/login", data={
                    "username": "testuser",
                    "password":"testuser"
                    })
    def test_home_anon(self):
        """Does home route without a logged in poet return correct page"""
        with self.client as c:
            c.get('/logout')
            resp = c.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Join the community',resp.data)
    def test_home_poet(self):
        """DOes home route with logged in poet work"""
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Add your wisdom',resp.data)
    
    def test_account_info(self):
        """Doers the account info page work with logged in poet"""
        with self.client as c:
            resp = c.get('/account')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Testuser's Account",resp.data)
    
    def test_Accout_info_no_poet(self):
        """Does the account infor page not allow non-logged in users"""
        with self.client as c:
            c.get('/logout')
            resp = c.get('/account', follow_redirects=True)

            # self.assertEqual(resp.status_code, 302)
            self.assertIn(b"You must login to access this page",resp.data)


import os
import unittest

from datetime import date
 
from telelegal_app import app, db, bcrypt
from telelegal_app.models import User, Profile, Forum, Requests

"""
Run these tests with the command:
python3 -m unittest telelegal_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_forum_post():
    a1 = Forum(title="First post", post="First forum post ever!")
    db.session.add(a1)
    db.session.commit()

def create_request():
    r1 = Requests(full_name="John Smith", city="Anytown, USA", email="johnsmith@domain.com", description="Here is my case.")
    db.session.add(r1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the books show up on the homepage."""
        # Set up
        create_user()

        # Make a GET request
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        response_text = response.get_data(as_text=True)
        self.assertNotIn('Log Out', response_text)

 
    def test_homepage_logged_in(self):
        """Test that the sign in/up buttons don't show up on the homepage."""
        # Set up
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
 
        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Sign in', response_text)
        self.assertNotIn('Sign up', response_text)



    
import os
from unittest import TestCase

from datetime import date
 
from books_app import app, db, bcrypt
from books_app.models import Book, Author, User, Audience

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def create_books():
    a1 = Author(name='Harper Lee')
    b1 = Book(
        title='To Kill a Mockingbird',
        publish_date=date(1960, 7, 11),
        author=a1
    )
    db.session.add(b1)

    a2 = Author(name='Sylvia Plath')
    b2 = Book(title='The Bell Jar', author=a2)
    db.session.add(b2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # A test for the signup route:
        # - Make a POST request to /signup, sending a username & password
        # - Check that the user now exists in the database
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/signup', data=post_data)

        user = User.query.filter_by(username='me1').one()

        password_check = bcrypt.check_password_hash(user.password, 'password')
        self.assertEqual(user.username, 'me1')
        self.assertTrue(password_check)


    def test_signup_existing_user(self):
        # Write a test for the signup route. It should:
        # - Create a user
        create_user()
        # - Make a POST request to /signup, sending the same username & password
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        # Convert reloaded page with error message into text
        signup_page = self.app.post('/signup', data=post_data, follow_redirects=True)
        page_text = signup_page.get_data(as_text=True)

        # Check that the form is displayed again with an error message
        self.assertIn('That username is taken. Please choose a different one.', page_text)

    def test_login_correct_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        create_user()
        # - Make a POST request to /login, sending the created username & password
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)
        # - Check that the "login" button is not displayed on the homepage
        self.assertNotIn('Log In', login_page_text)

    def test_login_nonexistent_user(self):
        # TODO: Write a test for the login route. It should:
        # - Make a POST request to /login, sending a username & password
        post_data = {
            'username': 'nonexistent_user',
            'password': 'password'
        }
        # - Check that the login form is displayed again, with an appropriate
        #   error message
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)
        self.assertIn('No user with that username. Please try again.', login_page_text)
        

    def test_login_incorrect_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        create_user()
        # - Make a POST request to /login, sending the created username &
        #   an incorrect password
        post_data = {
            'username': 'me1',
            'password': 'wrong_password'
        }
        # - Check that the login form is displayed again, with an appropriate
        #   error message
        login_page = self.app.post('/login', data=post_data, follow_redirects=True)
        login_page_text = login_page.get_data(as_text=True)
        self.assertIn("Password doesn&#39;t match. Please try again.", login_page_text)

    def test_logout(self):
        # TODO: Write a test for the logout route. It should:
        # - Create a user
        create_user()
        # - Log the user in (make a POST request to /login)
        # - Make a GET request to /logout
        # - Check that the "login" button appears on the homepage
        pass

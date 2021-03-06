"""Create database models to represent tables."""
from telelegal_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)



class User(UserMixin, db.Model):
    """User model, for attorneys only)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # One-to-many relationship: each user can have many forum posts
    forum_posts = db.relationship('Forum', back_populates='author')
    # One-to-one relationship: each user has exactly one profile
    profile = db.relationship('Profile', back_populates='user')

    def __repr__(self):
        return f'<Attorney: {self.username}>'

class Profile(db.Model):
    """Attorney profile model."""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False, unique=True)
    law_firm = db.Column(db.String(80), nullable=True)
    state_bar_num = db.Column(db.Integer, nullable=False)
    practice_areas = db.Column(db.String(300), nullable=False)
    years_exp = db.Column(db.Integer, nullable=False)
    # One-to-one relationship: each user has exactly one profile
    user = db.relationship('User', back_populates='profile')



class Forum(db.Model):
    """Forum model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    post = db.Column(db.String(1000), nullable=False)
    publish_date = db.Column(db.Date)

    # One-to-many relationship: each user can have many forum posts
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Attorney', back_populates='forum_posts')

    def __str__(self):
        return f'<Forum Post: {self.title}>'

    def __repr__(self):
        return f'<Forum Post: {self.title}>'



class Requests(db.Model):
    """Requests model."""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)



# FUTURE: Consider using flask-user library for multiple user types (attorney and potential client)


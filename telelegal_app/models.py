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

# class Audience(FormEnum):
#     CHILDREN = 'Children'
#     YOUNG_ADULT = 'Young Adult'
#     ADULT = 'Adult'
#     ALL = 'All'

class Forum(db.Model):
    """Forum model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    post = db.Column(db.String(1000), nullable=False)
    publish_date = db.Column(db.Date)

    # The author - Which attorney wrote it?
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Attorney', back_populates='forum_posts')

    def __str__(self):
        return f'<Forum Post: {self.title}>'

    def __repr__(self):
        return f'<Forum Post: {self.title}>'

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attorney_id = db.Column(db.Integer, db.ForeignKey('attorney.id'), nullable=False)
    author = db.relationship('Attorney', back_populates='forum_posts')



class Attorney(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    messages = db.Column(db.String(200), nullable=False)
    forum_posts = db.relationship('Forum', back_populates='author')
    favorite_books = db.relationship(
        'Book', secondary='user_book', back_populates='users_who_favorited')

    def __repr__(self):
        return f'<Attorney: {self.username}>'

class PClient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_books = db.relationship(
        'Book', secondary='user_book', back_populates='users_who_favorited')

    def __repr__(self):
        return f'<Potential Client: {self.username}>'

messages_table = db.Table('messages',
    db.Column('attorney_id', db.Integer, db.ForeignKey('attorney.id')),
    db.Column('pclient_id', db.Integer, db.ForeignKey('pclient.id'))
)

# FUTURE: Consider using flask-user library 

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pwd_hash = db.Column(db.String(200))
    email = db.Column(db.String(256), unique=True)
    is_active = db.Column(db.Boolean, default=False)
    urole = db.Column(db.Enum(80))


    def __init__(self, username, pwd_hash, email, is_active, urole):
        self.username = username
        self.pwd_hash = pwd_hash
        self.email = email
        self.is_active = is_active
        self.urole = urole

    def get_id(self):
        return self.id
    # def is_active(self):
    #     return self.is_active
    def activate_user(self):
        self.is_active = True         
    def get_username(self):
        return self.username
    def get_urole(self):
        return self.urole

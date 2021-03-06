from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from telelegal_app.models import User, Forum, Requests

class ProfileForm(FlaskForm):
    """Form to create a public profile."""
    name = StringField('Genre Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')

class ForumForm(FlaskForm):
    """Form to create a forum post."""
    title = StringField('Book Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    publish_date = DateField('Date Published')
    author = QuerySelectField('Author',
        query_factory=lambda: Author.query, allow_blank=False)
    audience = SelectField('Audience', choices=Audience.choices())
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query)
    submit = SubmitField('Submit')


class RequestForm(FlaskForm):
    """Form to create a request for a case review."""
    full_name = StringField('Name of Potential Client',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('Author Biography')
    submit = SubmitField('Submit')

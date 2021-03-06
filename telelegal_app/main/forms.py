from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from telelegal_app.models import User, Forum, Requests

class ProfileForm(FlaskForm):
    """Form to create a public profile."""
    full_name = StringField('Full Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    law_firm = StringField('Law Firm')
    state_bar_num = IntegerField('State Bar Number', validators=[DataRequired()])
    practice_areas = StringField('Practice Areas')
    years_exp = IntegerField('Years of Experience')
    submit = SubmitField('Submit')

class ForumForm(FlaskForm):
    """Form to create a forum post."""
    title = StringField('Title',
        validators=[DataRequired()])
    post = StringField('Post',
        validators=[DataRequired()])
    publish_date = DateField('Date Published')
    author = QuerySelectField('User',
        query_factory=lambda: User.query, allow_blank=False)
    submit = SubmitField('Submit')


class RequestForm(FlaskForm):
    """Form to create a request for a case review."""
    full_name = StringField('Full Name',
        validators=[DataRequired()])
    city = StringField('City of Residence')
    email = StringField('Email Address',
        validators=[DataRequired(), Length(min=6)])
    description = TextAreaField('Description of Case or Issue (include location and date, if applicable)',
        validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')

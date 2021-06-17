"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from telelegal_app.models import User, Profile, Forum, Requests
from telelegal_app.main.forms import ProfileForm, ForumForm, RequestForm
from telelegal_app import bcrypt

# Import app and db from events_app package so that we can run app
from telelegal_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    """Homepage."""
    return render_template('home.html')


@main.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    """Create a public profile."""
    form = ProfileForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_profile = Profile(
            full_name=form.full_name.data,
            law_firm=form.law_firm.data,
            state_bar_num=form.state_bar_num.data,
            practice_areas=form.practice_areas.data,
            years_exp=form.years_exp.data
        )
        db.session.add(new_profile)
        db.session.commit()

        flash('New profile was created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_profile.id))
    return render_template('create_profile.html', form=form)


@main.route('/create_forum_post', methods=['GET', 'POST'])
@login_required
def create_forum_post():
    """Create a forum post (attorneys only)."""
    form = ForumForm()
    if form.validate_on_submit():
        new_post = Forum(
            title=form.title.data,
            post=form.post.data,
            publish_date=datetime.today,
            author=current_user.username
        )
        db.session.add(new_post)
        db.session.commit()

        flash('New post created successfully.')
        return redirect(url_for('main.forum'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_forum_post.html', form=form)


@main.route('/create_request', methods=['GET', 'POST'])
def create_request():
    """Create a request for a case to be reviewed by an attorney."""
    form = RequestForm()
    if form.validate_on_submit():
        new_request = Requests(
            full_name=form.full_name.data,
            city=form.city.data,
            email=form.email.data,
            description=form.description.data
        )
        db.session.add(new_request)
        db.session.commit()

        flash('New request submitted successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_request.html', form=form)


@main.route('/forum/<forum_id>', methods=['GET', 'POST'])
@login_required
def forum_post(forum_id):
    """Create a forum post."""
    forum_post = Forum.query.get(forum_id)
    form = ForumForm(obj=forum_post)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        forum_post.title = form.title.data
        forum_post.publish_date = form.publish_date.data
        forum_post.author = form.author.data
        forum_post.post = form.post.data

        db.session.commit()

        flash('Forum post was updated successfully.')
        return redirect(url_for('main.forum_post', forum_id=forum_id))

    return render_template('forum_post.html', forum_post=forum_post, form=form)


@main.route('/profile/<full_name>')
def profile(full_name):
    """View public profile of an attorny."""
    # user = User.query.filter_by(username=username).one()
    profile = Profile.query.filter_by(full_name=full_name).first()
    return render_template('profile.html', profile=profile)

@main.route('/directory')
def directory():
    """Directory page displaying list of all attorney profiles."""
    all_profiles = Profile.query.all()
    return render_template('directory.html',
        all_profiles=all_profiles)

@main.route('/forum')
@login_required
def forum():
    """View list of forum posts (attorneys only)."""
    all_forum_posts = Forum.query.all()
    return render_template('forum.html',
        all_forum_posts=all_forum_posts)

@main.route('/requests')
@login_required
def requests():
    """View list of all submitted requests (attorneys only)."""
    all_requests = Requests.query.all()
    return render_template('requests.html',
        all_requests=all_requests)

# Refactored route
@main.route('/requests/<request_id>')
@login_required
def view_request(request_id):
    """View an individual request within the list (attorneys only)."""
    request = Requests.query.filter_by(requests_id=request_id).first()
    return render_template('request.html', request=request)


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
    return render_template('home.html')


@main.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
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
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_forum_post.html', form=form)


@main.route('/create_request', methods=['GET', 'POST'])
def create_request():
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
    # user = User.query.filter_by(username=username).one()
    user = User.query.filter_by(full_name=full_name).first()
    return render_template('profile.html', user=user)


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
    return render_template('create_book.html', form=form)


@main.route('/create_forum_post', methods=['GET', 'POST'])
@login_required
def create_forum_post():
    form = ForumForm()
    if form.validate_on_submit():
        new_post = Forum(
            title=form.title.data,
            post=form.post.data,
            publish_date=form.publish_date.data,
            author=form.author.data
        )
        db.session.add(new_post)
        db.session.commit()

        flash('New post created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_author.html', form=form)


@main.route('/create_request', methods=['GET', 'POST'])
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        new_request = Requests(
            full_name=form.full_name.data,

        )
        db.session.add(new_request)
        db.session.commit()

        flash('New request submitted successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_genre.html', form=form)


@main.route('/forum/<forum_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.author = form.author.data
        book.audience = form.audience.data
        book.genres = form.genres.data

        db.session.commit()

        flash('Book was updated successfully.')
        return redirect(url_for('main.book_detail', book_id=book_id))

    return render_template('book_detail.html', book=book, form=form)


@main.route('/profile/<username>')
def profile(username):
    # user = User.query.filter_by(username=username).one()
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)


@main.route('/favorite/<book_id>', methods=['POST'])
@login_required
def favorite_book(book_id):
    book = Book.query.get(book_id)
    if book in current_user.favorite_books:
        flash('Book already in favorites.')
    else:
        current_user.favorite_books.append(book)
        db.session.add(current_user)
        db.session.commit()
        flash('Book added to favorites.')
    return redirect(url_for('main.book_detail', book_id=book_id))


@main.route('/unfavorite/<book_id>', methods=['POST'])
@login_required
def unfavorite_book(book_id):
    book = Book.query.get(book_id)
    if book not in current_user.favorite_books:
        flash('Book not in favorites.')
    else:
        current_user.favorite_books.remove(book)
        db.session.add(current_user)
        db.session.commit()
        flash('Book removed from favorites.')
    return redirect(url_for('main.book_detail', book_id=book_id))

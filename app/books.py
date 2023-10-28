import bleach
import markdown
import os
import sqlalchemy as sa
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import app as my_app, db as my_db
from auth import permission_check as my_permission_check
from models import Book as my_Book, Genre as my_Genre, User as my_User, Review as my_Review, Image as my_Image, Collection as my_Collection
from tools import BooksFilter as my_BooksFilter, ImageSaver as my_ImageSaver

blueP = Blueprint('books', __name__, url_prefix='/books')
PER_page_books = 9

BOOK_parameter = ['author', 'name',
                  'publishing_house', 'volume', 'creationd_at']


def my_search_parameters():
    return {
        'name': request.args.get('name'),
        'genre_ids': request.args.getlist('genre_ids'),
    }


@blueP.route('/')
def index_file():
    page_books = request.args.get('page_books', 1, type=int)
    books = my_BooksFilter(**my_search_parameters()).perform()
    reviews_books_count = {}
    for book in books:
        reviews_books_count[book.id] = len(book.reviews_books)
    pagination = books.paginate(page_books, PER_page_books)
    books = pagination.items
    genres = my_Genre.query.all()
    return render_template('books/index_file.html',
                           books=books,
                           genres=genres,
                           pagination=pagination,
                           search_parameters=my_search_parameters(),
                           reviews_books_count=reviews_books_count)


def my_parameter():
    return {p: request.form.get(p) for p in BOOK_parameter}


@blueP.route('/creation', methods=['POST'])
@login_required
@my_permission_check('creation')
def creation():
    f = request.files.get('background_img')
    img = None
    if f and f.filename:
        img = my_ImageSaver(f).save()

    try:
        genres = request.form.getlist('genres')
        genres = list(map(my_Genre.query.get, genres))
        short_desc = markdown.markdown(
            bleach.clean(request.form.get('short_desc')))
        book = my_Book(**my_parameter())
        book.genres = genres
        book.short_desc = short_desc

        if not img:
            my_db.session.rollback()
            flash('Select a picture', 'danger')
            genres = my_Genre.query.all()
            return render_template('books/new_books.html',
                                   genres=genres, book=book)

        book.background_image_id = img.id

        for key in BOOK_parameter:
            if not getattr(book, key) or not book.short_desc or not book.genres:
                my_db.session.rollback()
                flash('Fill in all the fields', 'danger')
                genres = my_Genre.query.all()
                return render_template('books/new_books.html',
                                       genres=genres, book=book)

        my_db.session.add(book)
        my_db.session.commit()
        flash(f'A book "{book.name}" has been successfully added!', 'success')

    except sa.exc.SQLAlchemyError:
        my_db.session.rollback()
        flash(f'An error occurred while saving the book', 'danger')
        genres = my_Genre.query.all()
        return render_template('books/new_books.html',
                               genres=genres, book=book)
    return redirect(url_for('books.index_file'))


@blueP.route('/<int:book_id>/edit_books')
@login_required
@my_permission_check('update_books')
def edit_books(book_id):
    book = my_Book.query.get(book_id)
    genres = my_Genre.query.all()
    return render_template('books/update_books.html',
                           book=book,
                           genres=genres)


@blueP.route('/new_books')
@login_required
@my_permission_check('creation')
def new_books():
    genres = my_Genre.query.all()
    return render_template('books/new_books.html',
                           genres=genres,
                           book={})


@blueP.route('/<int:book_id>')
def show(book_id):
    book = my_Book.query.get(book_id)
    reviews_books_count = len(book.reviews_books)
    user_review = my_Review()
    collections = my_Collection.query.filter_by(user_id=current_user.id)
    if current_user.is_authenticated:
        user_review = my_Review.query.filter_by(
            user_id=current_user.id).filter_by(book_id=book_id).first()
    book_reviews_books = my_Review.query.filter_by(book_id=book_id).order_by(
        my_Review.creationd_at.desc()).limit(5).all()
    return render_template('books/show.html', book=book,
                           review=user_review, book_reviews_books=book_reviews_books, reviews_books_count=reviews_books_count, collections=collections)


@blueP.route('/<int:book_id>/delete_books', methods=['POST'])
@login_required
@my_permission_check('delete_books')
def delete_books(book_id):
    book = my_Book.query.get(book_id)
    books_image = my_Book.query.filter_by(
        background_image_id=book.bg_image.id).count()
    try:
        my_db.session.delete_books(book)

        if book.background_image_id:
            if books_image == 1:
                image = my_Image.query.get(book.background_image_id)
                if image:
                    os.remove(os.path.join(my_app.config['UPLOAD_FOLDER'],
                                           image.storage_filename))
                my_db.session.delete_books(image)
        my_db.session.commit()
        flash(f'A book "{book.name}" successfully delete_booksd', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'An error occurred while deleting the book', 'danger')
        my_db.session.rollback()
        return render_template('books/index_file.html')
    return redirect(url_for('books.index_file'))


@blueP.route('/<int:book_id>/send', methods=['POST'])
@login_required
def send_review_books(book_id):
    try:
        text = markdown.markdown(bleach.clean(request.form.get('text_review')))
        rating = int(request.form.get('rating_id'))
        review = my_Review(text=text, rating=rating,
                           book_id=book_id, user_id=current_user.id)
        my_db.session.add(review)
        book = my_Book.query.get(book_id)
        book.rating_up(rating)
        my_db.session.commit()
        flash(f'Your review has been successfully sent!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'There was an error sending your review', 'danger')
        my_db.session.rollback()
        book = my_Book.query.get(book_id)
        user = my_User.query.get(current_user.id)
        return render_template('books/give_review_books.html',
                               book=book,
                               user=user)
    return redirect(url_for('books.show', book_id=book_id))


@blueP.route('/<int:book_id>/updating', methods=['POST'])
@login_required
@my_permission_check('update_books')
def update_books(book_id):
    parametres = my_parameter().items()
    print('='*30, '\n', parametres)
    try:
        book = my_Book.query.get(book_id)
        genres = request.form.getlist('genres')
        genres = list(map(my_Genre.query.get, genres))
        for key, value in parametres:
            if value:
                setattr(book, key, value)
        book.genres = genres
        for key in BOOK_parameter:
            if not getattr(book, key) or not book.short_desc or not book.genres:
                my_db.session.rollback()
                flash('All fields must be completed', 'danger')
                genres = my_Genre.query.all()
                return render_template('books/update_books.html',
                                       genres=genres, book=book)
        my_db.session.commit()
        flash(f'Книга {book.name} has been successfully changed!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'An error occurred while saving the book', 'danger')
        my_db.session.rollback()
        book = my_Book.query.get(book_id)
        genres = my_Genre.query.all()
        return render_template('books/update_books.html',
                               book=book,
                               genres=genres)
    return redirect(url_for('books.show', book_id=book.id))


@blueP.route('/<int:book_id>/reviews_books')
def reviews_books(book_id):
    page_books = request.args.get('page_books', 1, type=int)
    book_reviews_books = my_Review.query.filter_by(book_id=book_id)
    sort_reviews_books = request.args.get('sort_reviews_books')
    dictionary_reviews_books = {
        'reviews_books_filter': sort_reviews_books, 'book_id': book_id}
    if sort_reviews_books == 'positive':
        book_reviews_books = book_reviews_books.order_by(
            my_Review.rating.desc())
    elif sort_reviews_books == 'negative':
        book_reviews_books = book_reviews_books.order_by(
            my_Review.rating.asc())
    else:
        book_reviews_books = book_reviews_books.order_by(
            my_Review.creationd_at.desc())
    pagination = book_reviews_books.paginate(page_books, 5)
    book_reviews_books = pagination.items
    return render_template('books/reviews_books.html',
                           book_reviews_books=book_reviews_books, book_id=book_id,
                           pagination=pagination, parameter=dictionary_reviews_books)


@blueP.route('/<int:book_id>/give_review_books')
@login_required
def give_review_books(book_id):
    book = my_Book.query.get(book_id)
    user = my_User.query.get(current_user.id)
    return render_template('books/give_review_books.html',
                           book=book,
                           user=user)

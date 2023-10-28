from flask import Blueprint, render_template, request, flash, redirect, url_for

import sqlalchemy as sa


from auth import permission_check

from tools import ImageSaver, BooksFilter

from flask_login import current_user, login_required

from models import Book, Genre, User, Review, Image, Collection

from app import db


bluep = Blueprint('collections', __name__, url_prefix='/collections')


def params_search():
    return {
        'name': request.args.get('name'),
        'genre_ids': request.args.getlist('genre_ids'),
    }


@bluep.route('/')
@login_required
@permission_check('show_collections')
def display_index():
    page_books = request.args.get('page_books', 1, type=int)
    user_id = current_user.id
    user_collections = Collection.query.filter_by(user_id=user_id)
    books_count = {}
    for collection in user_collections:
        books_count[collection.id] = len(collection.books)
    pagination = user_collections.paginate(page_books, 4)
    user_collections = pagination.items
    return render_template('collections/index.html',
                           collections=user_collections,
                           search_params={},
                           pagination=pagination,
                           books_count=books_count)


@bluep.route('/create', methods=['POST'])
@login_required
@permission_check('show_collections')
def create_collection():
    try:
        name = request.form.get('name')
        desc = request.form.get('desc')
        collection = Collection(user_id=current_user.id, name=name, desc=desc)
        db.session.add(collection)
        db.session.commit()
        flash(
            f'Selection "{collection.name}" was added successfully!', 'success')
    except sa.exc.SQLAlchemyError:
        flash(f'An error occurred while adding the collection', 'danger')
        db.session.rollback()
    return redirect(url_for('collections.index'))


@bluep.route('/<int:book_id>/add_book', methods=['POST'])
@login_required
@permission_check('show_collections')
def add_book_to_collection(book_id):
    change_collection = request.form.get('collection_id')
    try:
        collection = Collection.query.get(change_collection)
        book = Book.query.get(book_id)
        collection.books.append(book)
        db.session.commit()
        flash(
            f'A book"{book.name}" has been added to the collection"{collection.name}"!', 'success')
    except sa.exc.SQLAlchemyError:
        flash('An error occurred when adding a book to the collection', 'danger')
        db.session.rollback()
    return redirect(url_for('books.show', book_id=book_id))


@bluep.route('/<int:collection_id>')
@login_required
@permission_check('show_collections')
def show_selected_collection(collection_id):
    collection = Collection.query.get(collection_id)
    books = collection.books
    reviews_count = {}
    for book in books:
        reviews_count[book.id] = len(book.reviews)
    genres = Genre.query.all()
    return render_template('collections/show_collection.html',
                           collection=collection,
                           genres=genres,
                           books=books,
                           reviews_count=reviews_count,
                           search_params=params_search())

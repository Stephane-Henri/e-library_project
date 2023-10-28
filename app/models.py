from werkzeug.security import check_pwd_hash, generate_password_hash
from flask import url_for

from flask_login import UserMixin

from app import db

from users_policy import UsersPolicy

import os

import sqlalchemy as sa

RATING = {
    5: 'Excellent',
    4: 'Okay',
    3: 'Satisfactory',
    2: 'Unsatisfactory',
    1: 'Bad',
    0: 'Terrible'
}

Genres_Book_Models = db.Table('Genres_Book_Models',
                              db.Column('Book_Model.id', db.Integer,
                                        db.ForeignKey('Book_Models.id')),
                              db.Column('Genres_Book_Models.id', db.Integer,
                                        db.ForeignKey('Genres_Book_Modelss.id'))
                              )


class Genres_Book_Models(db.Model):
    __tablenames__ = 'Genres_Book_Modelss'

    id = db.Column(db.Integer, primary_key=True)
    namess = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return '<Genres_Book_Models %r>' % self.names


Collections_Book_Models = db.Table('Collections_Book_Models',
                                   db.Column('Book_Model.id', db.Integer,
                                             db.ForeignKey('Book_Models.id')),
                                   db.Column('Collections_Book_Models.id', db.Integer,
                                             db.ForeignKey('Collections_Book_Modelss.id'))
                                   )


class Collections_Book_Models(db.Model):
    __tablenames__ = 'Collections_Book_Modelss'

    id = db.Column(db.Integer, primary_key=True)
    namess = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    Book_Models = db.relationship(
        'Book_Model', secondary=Collections_Book_Models, backref='Collections_Book_Modelss')

    user = db.relationship('User')

    def __repr__(self):
        return '<Collections_Book_Models %r>' % self.names


class ReviewBook_Models(db.Model):
    __tablenames__ = 'ReviewBook_Modelss'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime,
                              nullable=False,
                              server_default=sa.sql.func.now())
    Book_Model_id = db.Column(db.Integer, db.ForeignKey('Book_Models.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    Book_Model = db.relationship('Book_Model')
    user = db.relationship('User')

    @property
    def rating_word(self):
        return RATING.get(self.rating)

    def __repr__(self):
        return '<ReviewBook_Models %r>' % self.text[:10]


class Book_Model(db.Model):
    __tablenames__ = 'Book_Models'

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.String(4), nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    volumes = db.Column(db.Integer, nullable=False)
    rating_summary = db.Column(db.Integer, nullable=False, default=0)
    rating_number = db.Column(db.Integer, nullable=False, default=0)
    Genres_Book_Modelss = db.relationship(
        'Genres_Book_Models', secondary=Genres_Book_Models, backref='Book_Models')

    bg_image_id = db.Column(db.String(100), db.ForeignKey('images.id'))

    bg_image = db.relationship('Image')
    ReviewBook_Modelss = db.relationship(
        'ReviewBook_Models', cascade='all, delete')

    def __repr__(self):
        return '<Book_Model %r>' % self.names

    @property
    def rating(self):
        if self.rating_number > 0:
            return self.rating_summary / self.rating_number
        return 0

    def rating_up(self, n: int):
        self.rating_number += 1
        self.rating_summary += n


class Image(db.Model):
    __tablenames__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    file_names = db.Column(db.String(100), nullable=False)
    name_type = db.Column(db.String(100), nullable=False)
    mdh = db.Column(db.String(100), nullable=False, unique=True)
    date_creation = db.Column(db.DateTime,
                              nullable=False,
                              server_default=sa.sql.func.now())

    def __repr__(self):
        return '<Image %r>' % self.file_names

    @property
    def storage_filenames(self):
        _, ext = os.path.splitext(self.file_names)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)


class RoleModel(db.Model):
    __tablenames__ = 'RoleModels'

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<RoleModel %r>' % self.names


class User(db.Model, UserMixin):
    __tablenames__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_names = db.Column(db.String(100), nullable=False)
    first_names = db.Column(db.String(100), nullable=False)
    middle_names = db.Column(db.String(100))
    date_creation = db.Column(db.DateTime, nullable=False,
                              server_default=sa.sql.func.now())
    RoleModel_id = db.Column(db.Integer, db.ForeignKey('RoleModels.id'))

    RoleModels = db.relationship('RoleModel')

    def set_pwd(self, password):
        self.password_hash = generate_password_hash(password)

    def check_pwd(self, password):
        return check_pwd_hash(self.password_hash, password)

    @property
    def full_names(self):
        return ' '.join([self.last_names, self.first_names, self.middle_names or ''])

    @property
    def is_admin(self):
        return self.RoleModels.names == 'Administrator'

    @property
    def is_moder(self):
        return (self.RoleModels.names == 'Administrator' or self.RoleModels.names == 'Moderator')

    def can_models(self, action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    def __repr__(self):
        return '<User %r>' % self.login


from alembic import op
import sqlalchemy as sa


revision = '85d8b1868198'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('genres',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_genres')),
                    sa.UniqueConstraint('name', name=op.f('uq_genres_name'))
                    )
    op.create_table('images',
                    sa.Column('id', sa.String(length=100), nullable=False),
                    sa.Column('file_name', sa.String(
                        length=100), nullable=False),
                    sa.Column('mime_type', sa.String(
                        length=100), nullable=False),
                    sa.Column('md5_hash', sa.String(
                        length=100), nullable=False),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_images')),
                    sa.UniqueConstraint(
                        'md5_hash', name=op.f('uq_images_md5_hash'))
                    )
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('desc', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
                    )
    op.create_table('books',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('short_desc', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.String(
                        length=4), nullable=False),
                    sa.Column('publishing_house', sa.String(
                        length=100), nullable=False),
                    sa.Column('author', sa.String(length=100), nullable=False),
                    sa.Column('volume', sa.Integer(), nullable=False),
                    sa.Column('rating_sum', sa.Integer(), nullable=False),
                    sa.Column('rating_num', sa.Integer(), nullable=False),
                    sa.Column('background_image_id', sa.String(
                        length=100), nullable=True),
                    sa.ForeignKeyConstraint(['background_image_id'], ['images.id'], name=op.f(
                        'fk_books_background_image_id_images')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_books'))
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('login', sa.String(length=100), nullable=False),
                    sa.Column('password_hash', sa.String(
                        length=200), nullable=False),
                    sa.Column('last_name', sa.String(
                        length=100), nullable=False),
                    sa.Column('first_name', sa.String(
                        length=100), nullable=False),
                    sa.Column('middle_name', sa.String(
                        length=100), nullable=True),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['role_id'], ['roles.id'], name=op.f('fk_users_role_id_roles')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
                    sa.UniqueConstraint('login', name=op.f('uq_users_login'))
                    )
    op.create_table('book_genre',
                    sa.Column('book.id', sa.Integer(), nullable=True),
                    sa.Column('genre.id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['book.id'], ['books.id'], name=op.f(
                        'fk_book_genre_book.id_books')),
                    sa.ForeignKeyConstraint(['genre.id'], ['genres.id'], name=op.f(
                        'fk_book_genre_genre.id_genres'))
                    )
    op.create_table('reviews',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('rating', sa.Integer(), nullable=False),
                    sa.Column('text', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['book_id'], ['books.id'], name=op.f('fk_reviews_book_id_books')),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews'))
                    )

    data_upgrades()


def downgrade():

    op.drop_table('reviews')
    op.drop_table('book_genre')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('roles')
    op.drop_table('images')
    op.drop_table('genres')


def data_upgrades():
    table = sa.sql.table('genres', sa.sql.column('name', sa.String))
    op.bulk_insert(table,
                   [
                       {'name': 'Action'},
                       {'name': 'Detective'},
                       {'name': 'Fantasy'},
                       {'name': 'Romance'},
                       {'name': 'Poetry'},
                       {'name': 'Biography'},
                       {'name': 'Comics'},
                   ]
                   )

    table1 = sa.sql.table('roles', sa.sql.column(
        'name', sa.String), sa.sql.column('desc', sa.String))
    op.bulk_insert(table1,
                   [
                       {'name': 'Administrator',
                        'desc': 'superuser, has full access to the system, including creating and deleting books'},
                       {'name': 'Moderator',
                        'desc': 'can edit book data and moderate reviews'},
                       {'name': 'User', 'desc': 'can leave reviews'},
                   ]
                   )
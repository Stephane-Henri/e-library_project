
from alembic import op
import sqlalchemy as sa


revision = '7baa03583ee2'
down_revision = '85d8b1868198'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('collections',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('desc', sa.Text(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f(
                        'fk_collections_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_collections')),
                    sa.UniqueConstraint(
                        'name', name=op.f('uq_collections_name'))
                    )
    op.create_table('book_collection',
                    sa.Column('book.id', sa.Integer(), nullable=True),
                    sa.Column('collection.id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['book.id'], ['books.id'], name=op.f(
                        'fk_book_collection_book.id_books')),
                    sa.ForeignKeyConstraint(['collection.id'], ['collections.id'], name=op.f(
                        'fk_book_collection_collection.id_collections'))
                    )


def downgrade():

    op.drop_table('book_collection')
    op.drop_table('collections')

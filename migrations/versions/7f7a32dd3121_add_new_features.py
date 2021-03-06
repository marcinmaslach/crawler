"""add new features

Revision ID: 7f7a32dd3121
Revises: 8b3fef4f7936
Create Date: 2019-11-24 21:47:05.521855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f7a32dd3121'
down_revision = '8b3fef4f7936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('viewed_flats_links', sa.String(), nullable=True))
    op.drop_column('users', 'viewed_floats_links')
    op.drop_column('users', 'viewed_floats_photos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('viewed_floats_photos', sa.VARCHAR(), nullable=True))
    op.add_column('users', sa.Column('viewed_floats_links', sa.VARCHAR(), nullable=True))
    op.drop_column('users', 'viewed_flats_links')
    # ### end Alembic commands ###

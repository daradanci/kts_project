"""changed gamescore points default value to 0

Revision ID: 872c1633856e
Revises: a38eb584302c
Create Date: 2023-03-19 20:31:01.434363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872c1633856e'
down_revision = 'a38eb584302c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('gamescores', 'points',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('gamescores', 'points',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
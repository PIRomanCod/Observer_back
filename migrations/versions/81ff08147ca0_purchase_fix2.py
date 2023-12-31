"""purchase fix2

Revision ID: 81ff08147ca0
Revises: 8f77add7eb3e
Create Date: 2023-11-24 11:35:58.072864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ff08147ca0'
down_revision = '8f77add7eb3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchases', 'notes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases', sa.Column('notes', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

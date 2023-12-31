"""purshase ajustment

Revision ID: b5eac1d7c951
Revises: 2e1ce866b9eb
Create Date: 2023-11-22 14:53:01.142165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5eac1d7c951'
down_revision = '2e1ce866b9eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases', sa.Column('quantity', sa.Float(), nullable=False))
    op.drop_column('purchases', 'quantity_tn')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases', sa.Column('quantity_tn', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('purchases', 'quantity')
    # ### end Alembic commands ###

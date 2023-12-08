"""del enum category

Revision ID: 27e3f0e99a5b
Revises: 47ed05167651
Create Date: 2023-11-30 15:20:13.003725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '27e3f0e99a5b'
# down_revision = '47ed05167651'
down_revision = '5ccef90fa113'

branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # op.add_column('transactions', sa.Column('expenses_category', sa.Enum('buyer', 'capital', 'fixed', 'interest', 'investments', 'invoice_job', 'old_debt', 'settlements', 'variable', 'other', name='expensestype'), nullable=False))
    # op.drop_column('transactions', 'expenses_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # op.add_column('transactions', sa.Column('expenses_type', postgresql.ENUM('buyer', 'capital', 'fixed', 'interest', 'investments', 'invoice_job', 'old_debt', 'settlements', 'variable', 'other', name='expensestype'), autoincrement=False, nullable=True))
    # op.drop_column('transactions', 'expenses_category')
    # ### end Alembic commands ###

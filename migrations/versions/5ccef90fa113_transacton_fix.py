"""transacton_fix

Revision ID: 5ccef90fa113
Revises: b4f74da1f8d1
Create Date: 2023-11-29 18:28:26.276832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ccef90fa113'
down_revision = 'b4f74da1f8d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('expenses_type', sa.Enum('buyer', 'capital', 'fixed', 'interest', 'investments', 'invoice_job', 'old_debt', 'settlements', 'variable', 'other', name='expensestype'), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('accounting_type', sa.Enum('GR Baris', 'ProOil', name='accounting_type'), nullable=False),
    sa.Column('operation_type', sa.Enum('debit', 'credit', name='operation_type'), nullable=False),
    sa.Column('document_type', sa.Enum('payment', 'invoice', 'changes', name='document_type'), nullable=False),
    sa.Column('operation_region', sa.Enum('domestic', 'export', 'import', name='operation_region'), nullable=False),
    sa.Column('currency', sa.Enum('tl', 'eur', 'usd', name='currency_type'), nullable=False),
    sa.Column('sum', sa.Float(), nullable=False),
    sa.Column('usd_tl_rate', sa.Numeric(precision=18, scale=4), nullable=False),
    sa.Column('eur_usd_rate', sa.Numeric(precision=18, scale=4), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###

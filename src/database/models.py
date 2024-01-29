import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, Enum, ForeignKey, Float, Date, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserRole(enum.Enum):
    admin: str = 'admin'
    user: str = 'user'


# class CompanyRole(enum.Enum):
#     buyer: str = 'buyer'
#     supplier: str = 'supplier'
#     partner: str = 'partner'
#     other: str = 'other'


# class AccountingType(enum.Enum):
#     GR: str = "GR"
#     OFFICIAL: str = "OFFICIAL"
#
#
# class TransactionType(enum.Enum):
#     D: str = "Debit"
#     C: str = "Credit"
#
#
# class DocumentType(enum.Enum):
#     invoice: str = "invoice"
#     payment: str = "payment"
#
#
# class OperationRegion(enum.Enum):
#     domestic: str = "domestic"
#     export: str = "export"
#     _import: str = "import"
#
#
# class AccountName(enum.Enum):
#     QNB: str = "QNB"
#     VAKIF: str = "VAKIF"
#     ZIRAAT: str = "ZIRAAT"
#     KUVEYT: str = "KUVEYT"
#     TRY_CASA: str = "TRY_CASA"
#     USD_CASA: str = "USD_CASA"
#     EUR_CASA: str = "EUR_CASA"
#     BGN_CASA: str = "BGN_CASA"
#
#
# class PaymentMethod(enum.Enum):
#     CASH: str = "CASH"
#     BANK_ACCOUNT: str = "BANK_ACCOUNT"
#     CREDIT_CARD: str = "CREDIT_CARD"
#
#
# class Currency(enum.Enum):
#     TL: str = "TL"
#     USD: str = "USD"
#     EUR: str = "EUR"
#     BGN: str = "BGN"
#
#
# class ExpensesType(enum.Enum):
#     buyer = "buyer"
#     capital = "capital"
#     fixed = "fixed"
#     interest = "interest"
#     investments = "investments"
#     invoice_job = "invoice_job"
#     old_debt = "old_debt"
#     settlements = "settlements"
#     variable = "variable"
#     other = "other"


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    company_name = Column(String(150), index=True, nullable=False, unique=True)
    additional_info = Column(String(150), nullable=True)
    favorite_role = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), default=1)
    user = relationship('User', backref='companies')


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), index=True, nullable=False)
    lastname = Column(String(50), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    additional_info = Column(String(150), nullable=True)
    # is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), default=1)
    user = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('user_roles', Enum(UserRole), default=UserRole.user)
    # roles = Column(Enum(UserRole), default=UserRole.user)
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# class Invoice(Base):
#     __tablename__ = "documents"
#     id = Column(Integer, primary_key=True)
#     document_number = Column(String(50), nullable=False)
#     document_date = Column(DateTime, nullable=False)
#     document_type = Column('document_type', Enum(DocumentType), default=DocumentType.invoice)
#     company_id = Column('company_id', ForeignKey('companies.id', ondelete='CASCADE'), default=1)
#     company = relationship('Company', backref='documents')
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
#     deleted_at = Column(DateTime, default=func.now(), onupdate=func.now())
#     is_deleted = Column(Boolean, default=False)
#     user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=1)
#     user = relationship('User', backref='documents')
#
#
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    expenses_category = Column(Enum("buyer", "capital", "fixed", "interest", "investments", "invoice_job", "old_debt",
                                    "settlements", "variable", "other", name='expensestype'), nullable=False) # Column(String(255), nullable=False)
    company_id = Column('company_id', ForeignKey('companies.id', ondelete='CASCADE'), default=1)
    company = relationship('Company', backref='transactions')
    description = Column(String(255), nullable=True)
    accounting_type = Column(Enum('GR Baris', 'ProOil', name='accounting_type'), nullable=False)
    operation_type = Column(Enum('debit', 'credit', name='operation_type'), nullable=False)
    document_type = Column(Enum('payment', 'invoice', 'changes', "undefined", name='document_types'), nullable=True)
    operation_region = Column(Enum('domestic', 'export', 'import', name='operation_region'), nullable=False)
    currency = Column(Enum('tl', 'eur', 'usd', name='currency_type'), nullable=False)
    sum = Column(Float, nullable=False)
    usd_tl_rate = Column(Numeric(precision=18, scale=4), nullable=False)
    eur_usd_rate = Column(Numeric(precision=18, scale=4), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=func.now())
    is_deleted = Column(Boolean, default=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='SET NULL'), default=1)
    user = relationship('User', backref='transactions')



class DailyStockReports(Base):
    __tablename__ = "DailyStockReports"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=func.now(), index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='SET NULL'), index=True)
    quantity = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    english_name = Column(String(100), nullable=False)
    ukrainian_name = Column(String(100), nullable=False)
    russian_name = Column(String(100), nullable=False)
    turkish_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', backref='products')


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    operation_type = Column(Enum('income', 'outcome', name='operation_types'), nullable=False)
    quantity = Column(Float, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='SET NULL'))
    company = relationship('Company', backref='purchases')
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Products', backref='purchases')
    price_tl = Column(Numeric(precision=18, scale=2), nullable=False)
    transfer_cost = Column(Numeric(precision=18, scale=2), nullable=True)
    commission_duties = Column(Numeric(precision=18, scale=2), nullable=True)
    sum_total_tl = Column(Numeric(precision=18, scale=2), nullable=False)
    appr_ex_rate = Column(Numeric(precision=18, scale=4), nullable=False)
    sum_total_usd = Column(Numeric(precision=18, scale=2), nullable=False)
    account_type = Column(String(50), nullable=False)
    cost_per_mt_tl = Column(Numeric(precision=18, scale=2), nullable=False)
    cost_per_mt_usd = Column(Numeric(precision=18, scale=2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', backref='purchases')


class ExchRate(Base):
    __tablename__ = "exchrates"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    usd_tl_rate = Column(Numeric(precision=18, scale=4), nullable=False)
    eur_usd_rate = Column(Numeric(precision=18, scale=4), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='SET NULL'), default=1)
    user = relationship('User', backref='exch_rates')


class AccountName(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = relationship('User', backref='accounts')


class Movements(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    company_id = Column('company_id', ForeignKey('companies.id', ondelete='SET NULL'), nullable=True)
    company = relationship('Company', backref='movements')
    description = Column(String(255), default="payment", nullable=True)
    account_type = Column(String(50), nullable=False)
    operation_type = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    sum = Column(Float, nullable=False)
    payment_way = Column('payment_way', ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    account = relationship('AccountName', backref='movements')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = relationship('User', backref='movements')

# @event.listens_for(Company, 'before_insert')
# def updated_favorite(mapper, conn, target):
#
#     if target.firstname.startswith('My'):
#         target.is_favorite = True
#
#
# @event.listens_for(Company, 'before_update')
# def updated_favorite(mapper, conn, target):
#
#     if target.firstname.startswith('My'):
#         target.is_favorite = True

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, condecimal
from decimal import Decimal
from src.database.models import UserRole, Company, Contact, User, DailyStockReports, Products, Purchase


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str = 'Unknown'
    email: str = 'unknown@example.com'
    avatar: str = 'Unknown'
    roles: UserRole = "user"
    created_at: date | None
    updated_at: date | None

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class UserInDB(UserModel):
    hashed_password: str


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str


class ProductModel(BaseModel):
    id: int
    name: str
    # english_name: str
    # ukrainian_name: str
    # russian_name: str
    # turkish_name: str

    class Config:
        orm_mode = True


class DailyStockReportModel(BaseModel):
    # id: int
    date: date
    # product_id: int
    product: ProductModel
    quantity: float

    class Config:
        orm_mode = True


class CompanyCreateUpdate(BaseModel):
    company_name: str
    additional_info: Optional[str] = None
    favorite_role: Optional[str] = None

    class Config:
        orm_mode = True


# class CompanyResponse(CompanyCreateUpdate):
#     id: int
#     created_at: datetime
#     updated_at: datetime
#     user_id: int
#
#     class Config:
#         orm_mode = True
class CompanyResponse(BaseModel):
    company_name: str
    id: int

    class Config:
        orm_mode = True


class CompanyListResponse(BaseModel):
    items: List[CompanyResponse]

    class Config:
        orm_mode = True


class CompanyDetailResponse(BaseModel):
    company_name: str
    additional_info: Optional[str] = None
    favorite_role: Optional[str] = None
    id: int

    class Config:
        orm_mode = True


class PurchaseCreateUpdate(BaseModel):
    date: date
    operation_type: str
    quantity: float
    company_id: int
    product_id: int
    price_tl: Decimal
    transfer_cost: Optional[Decimal] = None
    commission_duties: Optional[Decimal] = None
    sum_total_tl: Decimal
    appr_ex_rate: Decimal
    sum_total_usd: Decimal
    account_type: str
    cost_per_mt_tl: Decimal
    cost_per_mt_usd: Decimal
    user_id: int


    class Config:
        orm_mode = True


class PurchaseCreate(PurchaseCreateUpdate):
    pass


class PurchaseUpdate(PurchaseCreateUpdate):
    pass


class PurchaseResponse(PurchaseCreateUpdate):
    id: int

    class Config:
        orm_mode = True


class PurchaseListResponse(BaseModel):
    items: List[PurchaseResponse]

    class Config:
        orm_mode = True


class PurchaseBase(BaseModel):
    date: datetime
    operation_type: str
    quantity: float
    company_id: int
    product_id: int
    price_tl: Decimal
    # transfer_cost: Decimal
    # commission_duties: Decimal
    sum_total_tl: Decimal
    appr_ex_rate: Decimal
    sum_total_usd: Decimal
    account_type: str
    cost_per_mt_tl: Decimal
    cost_per_mt_usd: Decimal
    user_id: int

    class Config:
        orm_mode = True


class ExpensesType(str, Enum):
    buyer: str = "buyer"
    capital: str = "capital"
    fixed: str = "fixed"
    interest: str = "interest"
    investments: str = "investments"
    invoice_job: str = "invoice_job"
    old_debt: str = "old_debt"
    settlements: str = "settlements"
    variable: str = "variable"
    other: str = "other"


class OperationType(str, Enum):
    debit: str = "debit"
    credit: str = "credit"


class DocumentType(str, Enum):
    payment: str = "payment"
    invoice: str = "invoice"
    changes: str = "changes"
    undefined: str = "undefined"


class OperationRegion(str, Enum):
    domestic: str = "domestic"
    export: str = "export"
    import_: str = "import"  # "import" є зарезервованим словом, тому використовуємо "import_"


class CurrencyType(str, Enum):
    tl: str = "tl"
    eur: str = "eur"
    usd: str = "usd"


class TransactionBase(BaseModel):
    date: date
    expenses_category: ExpensesType
    company_id: int
    description: Optional[str] = None
    accounting_type: str  # Вам може знадобитися змінити цей тип відповідно до реальних значень
    operation_type: OperationType
    document_type: Optional[DocumentType] = None
    operation_region: OperationRegion
    currency: CurrencyType
    sum: float
    usd_tl_rate: Decimal
    eur_usd_rate: Decimal
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    is_deleted: bool
    user_id: int = Field(default=1, ge=1)

    class Config:
        orm_mode = True


class TransactionCreateUpdate(BaseModel):
    date: date
    expenses_category: ExpensesType
    company_id: int
    description: Optional[str] = None
    accounting_type: str
    operation_type: OperationType
    document_type: Optional[DocumentType] = None
    operation_region: OperationRegion
    currency: CurrencyType
    sum: float
    usd_tl_rate: Decimal
    eur_usd_rate: Decimal
    is_deleted: bool
    user_id: int

    class Config:
        orm_mode = True


class TransactionResponse(BaseModel):
    id: int
    date: date
    expenses_category: ExpensesType
    company_id: int
    description: Optional[str] = None
    accounting_type: str  # Вам може знадобитися змінити цей тип відповідно до реальних значень
    operation_type: OperationType
    document_type: Optional[DocumentType] = None
    operation_region: OperationRegion
    currency: CurrencyType
    sum: float
    usd_tl_rate: Decimal
    eur_usd_rate: Decimal
    # created_at: datetime
    # updated_at: datetime
    # deleted_at: datetime
    is_deleted: bool
    user_id: int

    class Config:
        orm_mode = True


class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]

    class Config:
        orm_mode = True


class TurnoverResponse(BaseModel):
    company_id: int
    currency: CurrencyType
    accounting_type: str
    expenses_category: ExpensesType
    debit_turnover_tl: float
    credit_turnover_tl: float
    debit_turnover_usd: float
    credit_turnover_usd: float

    class Config:
        orm_mode = True


class TurnoverListResponse(BaseModel):
    items: List[TurnoverResponse]

    class Config:
        orm_mode = True


class ExchRateCreate(BaseModel):
    date: date
    usd_tl_rate: Decimal
    eur_usd_rate: Decimal
    user_id: Optional[int] = 1

    class Config:
        orm_mode = True


class ExchRateResponse(ExchRateCreate):
    id: int

    class Config:
        orm_mode = True
from typing import List
import os
import pathlib
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc, select, func, case, text, literal_column
from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, UserRole, Products, Company, Purchase, Transaction
from src.schemas import TransactionListResponse, TransactionResponse, TransactionCreateUpdate, TransactionBase, \
    CurrencyType, OperationRegion, DocumentType, OperationType, ExpensesType, TurnoverListResponse


async def create_transaction(transaction: TransactionCreateUpdate, current_user, db: Session) -> TransactionResponse:
    # Реалізація логіки для створення запису в базі даних
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


async def update_transaction(transaction_id: int, current_user, transaction_data, db: Session) -> TransactionResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_transaction = await get_transaction(transaction_id, current_user, db)
    if db_transaction is None:
        return None
    if transaction_data.expenses_category == 'other':
        transaction_data.expenses_category = ExpensesType.other

    for key, value in transaction_data.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


async def delete_transaction(transaction_id: int, current_user, db: Session) -> TransactionResponse:
    # Реалізація логіки для видалення запису з бази даних
    db_transaction = await get_transaction(transaction_id, current_user, db)
    if db_transaction is None:
        return None
    db.delete(db_transaction)
    db.commit()
    return db_transaction


async def get_transaction(transaction_id: int, current_user, db: Session) -> TransactionResponse:
    # Реалізація логіки для отримання одного запису з бази даних
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    return db_transaction


async def get_transactions(limit, offset, current_user, db: Session) -> TransactionListResponse:
    # Реалізація логіки для отримання всіх записів з бази даних
    db_transaction = db.query(Transaction).offset(offset).limit(limit).all()
    return db_transaction


async def get_transaction_by_company(company_id: int, limit: int, offset: int, current_user: User, db: Session) \
        -> TransactionListResponse:
    return db.query(Transaction).filter(
        Transaction.company_id == company_id,
    ).offset(offset).limit(limit).all()


async def get_transaction_by_period(start_date: date, end_date: date, limit: int, offset: int, current_user: User,
                                    db: Session) -> TransactionListResponse:
    return db.query(Transaction).filter(
        and_(
            Transaction.date >= start_date,
            Transaction.date <= end_date,
        )
    ).offset(offset).limit(limit).all()

    """
       SELECT
       company_id,
       currency,
       accounting_type,
       expenses_category,
       SUM(CASE WHEN operation_type = 'debit' AND currency = 'tl' THEN sum ELSE 0 END) AS debit_turnover_tl,
       SUM(CASE WHEN operation_type = 'credit' AND currency = 'tl' THEN sum ELSE 0 END) AS credit_turnover_tl,
       SUM(CASE WHEN operation_type = 'debit' AND currency = 'usd' THEN sum ELSE 0 END) AS debit_turnover_usd,
       SUM(CASE WHEN operation_type = 'credit' AND currency = 'usd' THEN sum ELSE 0 END) AS credit_turnover_usd
       FROM transactions
       GROUP BY company_id, currency, accounting_type, expenses_category;
       """



async def get_turnover_by_company(current_user: User, db: Session) -> TurnoverListResponse:
    result = (
        db.query(
            Transaction.company_id,
            Transaction.currency,
            Transaction.accounting_type,
            Transaction.expenses_category,
            func.sum(
                case((and_(Transaction.operation_type == 'debit', Transaction.currency == 'tl'), Transaction.sum),
                     else_=0)).label('debit_turnover_tl'),
            func.sum(
                case((and_(Transaction.operation_type == 'credit', Transaction.currency == 'tl'), Transaction.sum),
                     else_=0)).label('credit_turnover_tl'),
            func.sum(
                case((and_(Transaction.operation_type == 'debit', Transaction.currency == 'usd'), Transaction.sum),
                     else_=0)).label('debit_turnover_usd'),
            func.sum(case(
                (and_(Transaction.operation_type == 'credit', Transaction.currency == 'usd'), Transaction.sum),
                else_=0)).label('credit_turnover_usd')
        )
        .group_by(Transaction.company_id, Transaction.currency, Transaction.accounting_type,
                  Transaction.expenses_category)
        .all()
    )

    return result


async def get_turnover_by_company_in_period(
    start_date: date,
    end_date: date,
    current_user: User,
    db: Session,

) -> TurnoverListResponse:
    result = (
        db.query(
            Transaction.company_id,
            Transaction.currency,
            Transaction.accounting_type,
            Transaction.expenses_category,
            func.sum(
                case((and_(
                    Transaction.operation_type == 'debit',
                    Transaction.currency == 'tl',
                    Transaction.date.between(start_date, end_date)
                ), Transaction.sum), else_=0)
            ).label('debit_turnover_tl'),
            func.sum(
                case((and_(
                    Transaction.operation_type == 'credit',
                    Transaction.currency == 'tl',
                    Transaction.date.between(start_date, end_date)
                ), Transaction.sum), else_=0)
            ).label('credit_turnover_tl'),
            func.sum(
                case((and_(
                    Transaction.operation_type == 'debit',
                    Transaction.currency == 'usd',
                    Transaction.date.between(start_date, end_date)
                ), Transaction.sum), else_=0)
            ).label('debit_turnover_usd'),
            func.sum(
                case((and_(
                    Transaction.operation_type == 'credit',
                    Transaction.currency == 'usd',
                    Transaction.date.between(start_date, end_date)
                ), Transaction.sum), else_=0)
            ).label('credit_turnover_usd')
        )
        .group_by(Transaction.company_id, Transaction.currency, Transaction.accounting_type,
                  Transaction.expenses_category)
        .all()
    )
    return result

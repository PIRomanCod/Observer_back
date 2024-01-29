from typing import List
import os
import pathlib
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc, select, func, case, text, literal_column
from src.conf.config import settings

from src.database.models import User, UserRole, Products, Company, Purchase, Transaction, AccountName
from src.schemas import CurrencyType, OperationType, AccountsListResponse, AccountBase, AccountResponse, AccountCreateUpdate


async def create_account(account: AccountCreateUpdate, current_user, db: Session) -> AccountResponse:
    # Реалізація логіки для створення запису в базі даних
    db_account = AccountName(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


async def get_account(account_id: int, current_user, db: Session) -> AccountResponse:
    # Реалізація логіки для отримання одного запису з бази даних
    db_account = db.query(AccountName).filter(AccountName.id == account_id).first()
    return db_account


async def update_account(account_id: int, current_user, account_data, db: Session) -> AccountResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_account = await get_account(account_id, current_user, db)
    if db_account is None:
        return None

    for key, value in account_data.dict().items():
        setattr(db_account, key, value)
    db.commit()
    db.refresh(db_account)
    return db_account


async def delete_account(account_id: int, current_user, db: Session) -> AccountResponse:
    # Реалізація логіки для видалення запису з бази даних
    db_account = await get_account(account_id, current_user, db)
    if db_account is None:
        return None
    db.delete(db_account)
    db.commit()
    return db_account


async def get_accounts(limit, offset, current_user, db: Session) -> AccountsListResponse:
    # Реалізація логіки для отримання всіх записів з бази даних
    db_accounts = db.query(AccountName).offset(offset).limit(limit).all()
    return db_accounts

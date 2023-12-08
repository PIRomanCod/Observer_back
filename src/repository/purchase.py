from typing import List
import os
import pathlib
from datetime import date

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc, select
from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, UserRole, Products, Company, Purchase
from src.schemas import CompanyCreateUpdate, CompanyResponse, CompanyListResponse, CompanyDetailResponse, \
    PurchaseCreate, PurchaseUpdate, PurchaseResponse, PurchaseListResponse


async def create_purchase(purchase: PurchaseCreate, current_user, db: Session) -> PurchaseResponse:
    # Реалізація логіки для створення запису в базі даних
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


async def update_purchase(purchase_id: int, current_user, purchase_data, db: Session) -> PurchaseResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_purchase = await get_purchase(purchase_id, current_user, db)
    if db_purchase is None:
        return None
    for key, value in purchase_data.dict().items():
        setattr(db_purchase, key, value)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


async def delete_purchase(purchase_id: int, current_user, db: Session) -> PurchaseResponse:
    # Реалізація логіки для видалення запису з бази даних
    db_purchase = await get_purchase(purchase_id, current_user, db)
    if db_purchase is None:
        return None
    db.delete(db_purchase)
    db.commit()
    return db_purchase


async def get_purchase(purchase_id: int, current_user, db: Session) -> PurchaseResponse:
    # Реалізація логіки для отримання одного запису з бази даних
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    return db_purchase


async def get_purchases(limit, offset, current_user, db: Session) -> PurchaseListResponse:
    # Реалізація логіки для отримання всіх записів з бази даних
    db_purchase = db.query(Purchase).offset(offset).limit(limit).all()
    return db_purchase


async def get_purchases_by_company(company_id: int, limit: int, offset: int, current_user: User, db: Session):
    return db.query(Purchase).filter(
        Purchase.company_id == company_id,
    ).offset(offset).limit(limit).all()


async def get_purchases_by_product(product_id: int, limit: int, offset: int, current_user: User, db: Session):
    return db.query(Purchase).filter(
        Purchase.product_id == product_id,
    ).offset(offset).limit(limit).all()


async def get_purchases_by_period(start_date: date, end_date: date, limit: int, offset: int, current_user: User, db: Session):
    return db.query(Purchase).filter(
        Purchase.date >= start_date,
        Purchase.date <= end_date,
    ).offset(offset).limit(limit).all()

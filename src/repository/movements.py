from typing import List
import os
import pathlib
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc, select, func, case, text, literal_column
from src.conf.config import settings

from src.database.models import User, UserRole, Products, Company, Purchase, Transaction, AccountName, Movements
from src.schemas import CurrencyType, OperationType, MovementsResponse, MovementsBase, MovementsListResponse, MovementsCreateUpdate


async def create_movements(movements: MovementsCreateUpdate, current_user, db: Session) -> MovementsResponse:
    # Реалізація логіки для створення запису в базі даних
    db_movements = Movements(**movements.dict())
    db.add(db_movements)
    db.commit()
    db.refresh(db_movements)
    return db_movements


async def get_movement(movement_id: int, current_user, db: Session) -> MovementsResponse:
    # Реалізація логіки для отримання одного запису з бази даних
    db_movement = db.query(Movements).filter(Movements.id == movement_id).first()
    return db_movement


async def update_movements(movements_id: int, current_user, movements_data, db: Session) -> MovementsResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_movements = await get_movement(movements_id, current_user, db)
    if db_movements is None:
        return None

    for key, value in movements_data.dict().items():
        setattr(db_movements, key, value)
    db.commit()
    db.refresh(db_movements)
    return db_movements


async def delete_movements(movements_id: int, current_user, db: Session) -> MovementsResponse:
    # Реалізація логіки для видалення запису з бази даних
    db_movements = await get_movement(movements_id, current_user, db)
    if db_movements is None:
        return None
    db.delete(db_movements)
    db.commit()
    return db_movements


async def get_movements(limit, offset, current_user, db: Session) -> MovementsListResponse:
    # Реалізація логіки для отримання всіх записів з бази даних
    db_movements = db.query(Movements).offset(offset).limit(limit).all()
    return db_movements


async def get_movements_by_company(company_id: int, limit: int, offset: int, current_user: User, db: Session) \
        -> MovementsListResponse:
    return db.query(Movements).filter(
        Movements.company_id == company_id,
    ).offset(offset).limit(limit).all()


async def get_movements_by_payment_way(payment_way_id: int, limit: int, offset: int, current_user: User, db: Session) \
        -> MovementsListResponse:
    return db.query(Movements).filter(
        Movements.payment_way == payment_way_id,
    ).offset(offset).limit(limit).all()


async def get_movements_by_period(start_date: date, end_date: date, limit: int, offset: int, current_user: User,
                                    db: Session) -> MovementsListResponse:
    return db.query(Movements).filter(
        and_(
            Movements.date >= start_date,
            Movements.date <= end_date,
        )
    ).offset(offset).limit(limit).all()

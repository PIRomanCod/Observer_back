from typing import List
import os
import pathlib

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc

from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, UserRole, Products
from src.schemas import ProductModel


async def get_products(
        current_user,
        db: Session,
        language: str,):

    # Отримайте дані з бази даних за обраний період
    query = db.query(Products)
    products = query.all()

    # Створіть список об'єктів ProductModel
    product_models = [ProductModel(id=product.id, name=getattr(product, language)) for product in products]

    return product_models

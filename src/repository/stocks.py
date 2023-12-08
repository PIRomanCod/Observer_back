from typing import List
import os
import pathlib

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc

from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, UserRole, Products, DailyStockReports
from src.schemas import ProductModel, DailyStockReportModel
# from back.src.services.seeds.db_reader import get_daily_stock_reports


async def get_stocks_in_period(
        start_date,
        end_date,
        limit,
        offset,
        current_user,
        db: Session,
        language: str,
        product_ids) -> List[DailyStockReportModel] | None:

    # Отримайте дані з бази даних за обраний період
    query = (
        db.query(DailyStockReports)
        .join(Products, Products.id == DailyStockReports.product_id)
        .filter(and_(DailyStockReports.date.between(start_date, end_date)))
    )
    excluded_product_ids = [8, 11, 14, 15, 16]
    if product_ids:
        query = query.filter(DailyStockReports.product_id.in_(product_ids))
    else:
        query = query.filter(~DailyStockReports.product_id.in_(excluded_product_ids))

    daily_stock_reports = (
        query
        .order_by(asc(DailyStockReports.date))
        .limit(limit)
        .offset(offset)
        .all()
    )

    # Перетворіть дані в об'єкти моделі
    stocks = []
    for stock in daily_stock_reports:
        product_data = db.query(Products).filter(Products.id == stock.product_id).first()
        product_model = ProductModel(id=stock.product_id, name=getattr(product_data, language))
        stock_model = DailyStockReportModel(id=stock.id, date=stock.date, quantity=stock.quantity, product=product_model)
        stocks.append(stock_model)

    return stocks

from typing import List
import os
import pathlib

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc, asc, select
from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, UserRole, Products, Company
from src.schemas import CompanyCreateUpdate, CompanyResponse, CompanyListResponse, CompanyDetailResponse, \
    PurchaseCreateUpdate, PurchaseCreate, PurchaseUpdate, PurchaseResponse, PurchaseListResponse


async def get_company(db: Session, company_id: int):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    return db_company


async def get_companies(limit, offset, current_user, db: Session) -> List[CompanyListResponse] | None:
    companies = db.query(Company).offset(offset).limit(limit).all()
    return companies


async def create_company(company,  current_user, db: Session) -> CompanyResponse | None:
    db_company=Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


async def read_company(company_id, current_user, db: Session) -> CompanyDetailResponse | None:
    db_company = await get_company(db, company_id)
    if db_company:
        response = CompanyDetailResponse(
            company_name=db_company.company_name,
            additional_info=db_company.additional_info,
            favorite_role=db_company.favorite_role,
            id=db_company.id
        )
        return response
    return None


async def update_company(company_id, company: CompanyCreateUpdate, current_user, db: Session):
    db_company = await get_company(db, company_id)
    if db_company is None:
        return None
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company


async def delete_company(company_id: int, db: Session):
    db_company = await get_company(db, company_id)
    if db_company is None:
        return None
    db.delete(db_company)
    db.commit()
    return db_company


async def search_companies_by_name(company_name, current_user, db) -> List[CompanyDetailResponse]:
    db_companies = db.query(Company).filter(
            Company.company_name.ilike(f"%{company_name}%")).all()

    return db_companies

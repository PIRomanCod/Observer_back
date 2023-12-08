from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Body
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, DailyStockReports
from src.repository import products as repository_products
from src.schemas import ProductModel
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/products', tags=["products"])

allowed_get_products = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.get("/", response_model=List[ProductModel], description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_products), Depends(RateLimiter(times=10, seconds=60))])
async def get_products(
        language: str = Query("english_name", description="Language for product names"),
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):

    # Передайте фільтри у функцію get_stocks_in_period
    products = await repository_products.get_products(current_user, db, language)

    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    return products

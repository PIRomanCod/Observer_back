from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Body
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, DailyStockReports
from src.repository import stocks as repository_stocks
from src.schemas import DailyStockReportModel
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/stocks', tags=["stocks"])

allowed_get_stocks = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.post("/", response_model=List[DailyStockReportModel], description='No more than 10 requests per minute',
             status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_stocks), Depends(RateLimiter(times=10, seconds=60))])
async def get_stocks(
        start_date: date = Query(...),
        end_date: date = Query(...),
        language: str = Query("english_name", description="Language for product names"),
        product_ids: List[int] = None,
        limit: int = Query(10, le=250),
        current_user: User = Depends(auth_service.get_current_user),
        offset: int = 0,
        db: Session = Depends(get_db),
):
    # Перевірте, чи обрані дати в правильному порядку
    if start_date > end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date range")

    # Передайте фільтри у функцію get_stocks_in_period
    stocks = await repository_stocks.get_stocks_in_period(
        start_date, end_date, limit, offset, current_user, db, language, product_ids
    )

    if stocks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    return stocks

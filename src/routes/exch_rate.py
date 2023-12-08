from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date, datetime

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, ExchRate
from src.repository import transactions as repository_transaction
from src.schemas import ExchRateCreate, ExchRateResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/rates', tags=["rates"])

allowed_get_rate = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.post("/", response_model=ExchRateResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_rate), Depends(RateLimiter(times=10, seconds=60))])
async def create_exchrates(exchrates: List[ExchRateCreate], current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    for exchrate in exchrates:
        db_exchrate = ExchRate(**exchrate.dict())
        db.add(db_exchrate)
    db.commit()
    db.refresh(db_exchrate)
    return db_exchrate


@router.get("/{date}", response_model=ExchRateResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_rate), Depends(RateLimiter(times=10, seconds=60))])
async def get_exchrates_by_date(date: date, current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    db_exchrate = db.query(ExchRate).filter(
        ExchRate.date == date,
    ).first()
    if not db_exchrate:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_exchrate


@router.delete("/{date}", dependencies=[Depends(allowed_get_rate), Depends(RateLimiter(times=10, seconds=60))])
async def delete_transaction(date: date,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_exchrate = await get_exchrates_by_date(date, current_user, db)
    if db_exchrate is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    db.delete(db_exchrate)
    db.commit()
    return {"status": "success", "message": "Purchase deleted successfully"}



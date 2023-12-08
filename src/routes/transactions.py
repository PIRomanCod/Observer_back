from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, Transaction
from src.repository import transactions as repository_transaction
from src.schemas import TransactionCreateUpdate, TransactionResponse, TransactionListResponse, TurnoverListResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/transactions', tags=["transactions"])

allowed_get_transaction = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def create_transaction(transaction_data: TransactionCreateUpdate,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    return await repository_transaction.create_transaction(transaction_data, current_user, db)


@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def read_transaction(transaction_id: int, current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    db_transaction = await repository_transaction.get_transaction(transaction_id, current_user, db)

    if db_transaction is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_transaction


@router.put("/{transaction_id}", response_model=TransactionCreateUpdate, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionCreateUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
) -> TransactionResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_transaction = await repository_transaction.get_transaction(transaction_id, current_user, db)
    if db_transaction is None:
        return None
    for key, value in transaction_data.dict().items():
        if hasattr(db_transaction, key):
            setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}",
               # status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def delete_transaction(transaction_id: int,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_transaction = await repository_transaction.delete_transaction(transaction_id, current_user, db)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return {"status": "success", "message": "Purchase deleted successfully", "id": transaction_id}


@router.get("/",
            response_model=TransactionListResponse,
            description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_transaction),
                          Depends(RateLimiter(times=10, seconds=60))]
            )
async def read_transactions(
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_transaction = await repository_transaction.get_transactions(limit, offset, current_user, db)
    return {"items": db_transaction}


@router.get("/by_company/{company_id}", response_model=TransactionListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def read_transactions_by_company(
        company_id: int,
        offset: int = 0,
        limit: int = 2000,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_transaction = await repository_transaction.get_transaction_by_company(company_id, limit, offset, current_user, db)
    return {"items": db_transaction}


@router.post("/by_period", response_model=TransactionListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_transaction), Depends(RateLimiter(times=10, seconds=60))])
async def read_purchases_by_period(
        start_date: date,
        end_date: date,
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_transaction = await repository_transaction.get_transaction_by_period(start_date, end_date, limit, offset, current_user, db)
    return {"items": db_transaction}


@router.get("/turnover/", response_model=TurnoverListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(auth_service.get_current_user), Depends(RateLimiter(times=10, seconds=60))])
async def read_turnover_by_company(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_turnover = await repository_transaction.get_turnover_by_company(current_user, db)

    return {"items": db_turnover}


@router.get("/turnover/by_period", response_model=TurnoverListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(auth_service.get_current_user), Depends(RateLimiter(times=10, seconds=60))])
async def get_turnover_by_company_in_period(
        start_date: date,
        end_date: date,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_turnover = await repository_transaction.get_turnover_by_company_in_period(start_date, end_date, current_user, db)

    return {"items": db_turnover}


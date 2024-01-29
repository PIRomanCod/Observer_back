from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, Movements
from src.repository import movements as repository_movements
from src.schemas import MovementsBase, MovementsCreateUpdate, MovementsResponse, MovementsListResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/movements', tags=["movements"])

allowed_get_movements = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.post("/", response_model=MovementsResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def create_movements(movements_data: MovementsCreateUpdate,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    return await repository_movements.create_movements(movements_data, current_user, db)


@router.get("/{movements_id}", response_model=MovementsResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def read_movement(movements_id: int, current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    db_movements = await repository_movements.get_movement(movements_id, current_user, db)

    if db_movements is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_movements


@router.put("/{movements_id}", response_model=MovementsCreateUpdate, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def update_movements(
    movements_id: int,
    movements_data: MovementsCreateUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
) -> MovementsResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_movements = await repository_movements.update_movements(movements_id, current_user, movements_data, db)
    if db_movements is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_movements


@router.delete("/{movements_id}",
               # status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def delete_movements(movements_id: int,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_movements = await repository_movements.delete_movements(movements_id, current_user, db)
    if db_movements is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return {"status": "success", "message": "Movement deleted successfully", "id": movements_id}


@router.get("/",
            response_model=MovementsListResponse,
            description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_movements),
                          Depends(RateLimiter(times=10, seconds=60))]
            )
async def read_movements(
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_movements = await repository_movements.get_movements(limit, offset, current_user, db)
    return {"items": db_movements}



@router.get("/by_company/{company_id}", response_model=MovementsListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def read_movements_by_company(
        company_id: int,
        offset: int = 0,
        limit: int = 2000,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_movements = await repository_movements.get_movements_by_company(company_id, limit, offset, current_user, db)
    return {"items": db_movements}


@router.get("/by_payment_way/{payment_way_id}", response_model=MovementsListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def read_movements_by_payment_way(
        payment_way_id: int,
        offset: int = 0,
        limit: int = 2000,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_movements = await repository_movements.get_movements_by_payment_way(payment_way_id, limit, offset, current_user, db)
    return {"items": db_movements}


@router.post("/by_period", response_model=MovementsListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_movements), Depends(RateLimiter(times=10, seconds=60))])
async def read_movements_by_period(
        start_date: date,
        end_date: date,
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_movements = await repository_movements.get_movements_by_period(start_date, end_date, limit, offset, current_user, db)
    return {"items": db_movements}




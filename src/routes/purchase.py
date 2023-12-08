from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole
from src.repository import purchase as repository_purchase
from src.schemas import PurchaseCreate, PurchaseUpdate, PurchaseResponse, PurchaseListResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/purchase', tags=["purchase"])

allowed_get_purchase = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def create_purchase_endpoint(purchase_data: PurchaseCreate,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    return await repository_purchase.create_purchase(purchase_data, current_user, db)


@router.get("/{purchase_id}", response_model=PurchaseResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def read_purchase(purchase_id: int, current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    db_purchase = await repository_purchase.get_purchase(purchase_id, current_user, db)

    if db_purchase is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_purchase


@router.put("/{purchase_id}", response_model=PurchaseUpdate, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def update_purchase_endpoint(purchase_id: int, purchase_data: PurchaseUpdate,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_purchase = await repository_purchase.update_purchase(purchase_id, purchase_data, current_user, db)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_purchase


@router.delete("/{purchase_id}",
               # status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def delete_purchase_endpoint(purchase_id: int,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_purchase = await repository_purchase.delete_purchase(purchase_id, current_user, db)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return {"status": "success", "message": "Purchase deleted successfully", "id": purchase_id}


@router.get("/",
            response_model=PurchaseListResponse,
            description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_purchase),
                          Depends(RateLimiter(times=10, seconds=60))]
            )
async def read_purchases(
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_purchases = await repository_purchase.get_purchases(limit, offset, current_user, db)
    return {"items": db_purchases}


@router.get("/by_company/{company_id}", response_model=PurchaseListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def read_purchases_by_company(
        company_id: int,
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_purchases = await repository_purchase.get_purchases_by_company(company_id, limit, offset, current_user, db)
    return {"items": db_purchases}


# @router.get("/by_product/{product_id}", response_model=PurchaseListResponse, status_code=status.HTTP_200_OK,
#             dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
# async def read_purchases_by_product(
#         product_id: int,
#         offset: int = 0,
#         limit: int = 100,
#         current_user: User = Depends(auth_service.get_current_user),
#         db: Session = Depends(get_db)
# ):
#     db_purchases = await repository_purchase.get_purchases_by_product(product_id, limit, offset, current_user, db)
#     return {"items": db_purchases}
@router.post("/by_product", response_model=PurchaseListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def read_purchases_by_product(
        product_id: int,
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_purchases = await repository_purchase.get_purchases_by_product(product_id, limit, offset, current_user, db)
    return {"items": db_purchases}


# @router.get("/by_period/{start_date}/{end_date}/{offset}/{limit}", response_model=PurchaseListResponse, status_code=status.HTTP_200_OK,
#             dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
# async def read_purchases_by_period(
#         start_date: date,
#         end_date: date,
#         offset: int = 0,
#         limit: int = 100,
#         current_user: User = Depends(auth_service.get_current_user),
#         db: Session = Depends(get_db)
# ):
#     db_purchases = await repository_purchase.get_purchases_by_period(start_date, end_date, limit, offset, current_user, db)
#     return {"items": db_purchases}


@router.post("/by_period", response_model=PurchaseListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_purchase), Depends(RateLimiter(times=10, seconds=60))])
async def read_purchases_by_period(
        start_date: date,
        end_date: date,
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_purchases = await repository_purchase.get_purchases_by_period(start_date, end_date, limit, offset, current_user, db)
    return {"items": db_purchases}
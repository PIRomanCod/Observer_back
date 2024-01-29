from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from datetime import date

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole, AccountName
from src.repository import accounts as repository_accounts
from src.schemas import AccountBase, AccountResponse, AccountCreateUpdate, AccountsListResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/accounts', tags=["accounts"])

allowed_get_accounts = RoleAccess([UserRole.admin, UserRole.user])  # noqa



@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_accounts), Depends(RateLimiter(times=10, seconds=60))])
async def create_accounts(accounts_data: AccountCreateUpdate,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    return await repository_accounts.create_accounts(accounts_data, current_user, db)


@router.get("/{movements_id}", response_model=AccountResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_accounts), Depends(RateLimiter(times=10, seconds=60))])
async def read_account(account_id: int, current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    db_accounts = await repository_accounts.get_account(account_id, current_user, db)

    if db_accounts is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_accounts


@router.put("/{accounts_id}", response_model=AccountCreateUpdate, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_get_accounts), Depends(RateLimiter(times=10, seconds=60))])
async def update_account(
    account_id: int,
    account_data: AccountCreateUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
) -> AccountResponse:
    # Реалізація логіки для оновлення запису в базі даних
    db_accounts = await repository_accounts.update_account(account_id, current_user, account_data, db)
    if db_accounts is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_accounts


@router.delete("/{account_id}",
               # status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_get_accounts), Depends(RateLimiter(times=10, seconds=60))])
async def delete_account(account_id: int,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)
                                   ):
    db_accounts = await repository_accounts.delete_account(account_id, current_user, db)
    if db_accounts is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return {"status": "success", "message": "Account deleted successfully", "id": account_id}


@router.get("/",
            response_model=AccountsListResponse,
            description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_accounts),
                          Depends(RateLimiter(times=10, seconds=60))]
            )
async def read_accounts(
        offset: int = 0,
        limit: int = 100,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    db_accounts = await repository_accounts.get_accounts(limit, offset, current_user, db)
    return {"items": db_accounts}

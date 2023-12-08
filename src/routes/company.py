from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.conf import messages
from src.database.db import get_db
from src.database.models import User, UserRole
from src.repository import company as repository_company
from src.schemas import CompanyCreateUpdate, CompanyResponse, CompanyListResponse, CompanyDetailResponse
from src.services.auth.auth import auth_service
from src.services.auth.role import RoleAccess

router = APIRouter(prefix='/company', tags=["company"])

allowed_get_company = RoleAccess([UserRole.admin, UserRole.user])  # noqa


@router.get("/", response_model=CompanyListResponse, description='No more than 10 requests per minute',
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def read_companies(
        offset: int = 0,
        limit: int = 600,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    companies = await repository_company.get_companies(limit, offset, current_user, db)

    if companies is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    return {"items": companies}


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def create_company(company: CompanyCreateUpdate, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    db_company = await repository_company.create_company(company, current_user, db)
    return db_company


@router.get("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def read_company(company_id: int, current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    db_company = await repository_company.read_company(company_id, current_user, db)

    if db_company is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_company


@router.put("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def update_company(company_id: int, company: CompanyCreateUpdate,
                         current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    db_company = await repository_company.update_company(company_id, company, current_user, db)
    if db_company is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return db_company


@router.delete("/{company_id}",
               # status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def delete_company(company_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    db_company = await repository_company.delete_company(company_id, db)
    if db_company is None:
        raise HTTPException(status_code=404, detail=messages.NOT_FOUND)
    return {"status": "success", "message": "Company deleted successfully", "id": company_id}


@router.get("/search/", response_model=CompanyListResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_company), Depends(RateLimiter(times=10, seconds=60))])
async def search_companies_by_name(
        company_name: str,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    companies = await repository_company.search_companies_by_name(company_name, current_user, db)
    return {"items": companies}

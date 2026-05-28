from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.category_service import CategoryService
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithCount

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return CategoryService(db).create(data)


@router.get("", response_model=List[CategoryWithCount])
def list_categories(
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return CategoryService(db).get_all_with_count()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return CategoryService(db).get_by_id(category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return CategoryService(db).update(category_id, data)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    CategoryService(db).delete(category_id)

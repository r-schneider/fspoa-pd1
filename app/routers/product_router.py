from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.schemas.metrics_schema import LowStockAlert

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Cria novo produto"""
    return ProductService(db).create(data)


@router.get("", response_model=List[ProductListResponse])
def list_products(
    q: Optional[str] = Query(None, description="Busca por nome, SKU ou código de barras"),
    category_id: Optional[int] = Query(None),
    active: Optional[bool] = Query(None),
    low_stock: bool = Query(False, description="Filtrar apenas produtos com estoque baixo"),
    out_of_stock: bool = Query(False, description="Filtrar apenas produtos sem estoque"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Lista e filtra produtos"""
    return ProductService(db).search(q, category_id, active, low_stock, out_of_stock, skip, limit)


@router.get("/low-stock", response_model=List[LowStockAlert])
def get_low_stock_alerts(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Retorna alertas de estoque abaixo do mínimo"""
    products = ProductService(db).get_low_stock_alerts()
    return [
        LowStockAlert(
            product_id=p.id,
            product_name=p.name,
            sku=p.sku,
            current_stock=p.current_stock,
            minimum_stock=p.minimum_stock,
            deficit=p.minimum_stock - p.current_stock,
        )
        for p in products
    ]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return ProductService(db).get_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return ProductService(db).update(product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ProductService(db).delete(product_id)

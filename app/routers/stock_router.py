from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.services.stock_movement_service import StockMovementService
from app.schemas.stock_movement_schema import (
    StockEntryCreate, StockExitCreate, StockMovementResponse, StockMovementDetail
)
from app.enums.unit_measure_enum import MovementType

router = APIRouter(prefix="/stock", tags=["Movimentações de Estoque"])


@router.post("/entry", response_model=StockMovementResponse, status_code=201)
def register_entry(
    data: StockEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Registra entrada de estoque (compra, ajuste ou devolução)"""
    return StockMovementService(db).register_entry(data, current_user)


@router.post("/exit", response_model=StockMovementResponse, status_code=201)
def register_exit(
    data: StockExitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Registra saída de estoque (venda, baixa ou ajuste)"""
    return StockMovementService(db).register_exit(data, current_user)


@router.get("/history", response_model=List[StockMovementDetail])
def get_movement_history(
    product_id: Optional[int] = Query(None),
    movement_type: Optional[MovementType] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Histórico de movimentações com filtros"""
    return StockMovementService(db).get_history(product_id, movement_type, start_date, end_date, skip, limit)


@router.get("/history/{product_id}", response_model=List[StockMovementResponse])
def get_product_history(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Histórico de movimentações de um produto específico"""
    return StockMovementService(db).get_product_history(product_id, skip, limit)

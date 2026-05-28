from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

from app.enums.unit_measure_enum import MovementType, MovementDirection
from app.schemas.user_schema import UserResponse


class StockEntryCreate(BaseModel):
    """Entrada de estoque (compra ou devolução)"""
    product_id: int
    movement_type: MovementType
    quantity: int
    unit_cost: Optional[Decimal] = None
    reason: Optional[str] = None
    reference_document: Optional[str] = None

    @field_validator("movement_type")
    @classmethod
    def must_be_entry(cls, v):
        if v not in (MovementType.ENTRADA_COMPRA, MovementType.ENTRADA_AJUSTE, MovementType.ENTRADA_DEVOLUCAO):
            raise ValueError("Use StockExitCreate para saídas de estoque")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class StockExitCreate(BaseModel):
    """Saída de estoque (venda ou baixa)"""
    product_id: int
    movement_type: MovementType
    quantity: int
    unit_price: Optional[Decimal] = None
    reason: Optional[str] = None
    reference_document: Optional[str] = None

    @field_validator("movement_type")
    @classmethod
    def must_be_exit(cls, v):
        if v not in (MovementType.SAIDA_VENDA, MovementType.SAIDA_BAIXA, MovementType.SAIDA_AJUSTE):
            raise ValueError("Use StockEntryCreate para entradas de estoque")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class StockMovementResponse(BaseModel):
    id: int
    movement_type: MovementType
    direction: MovementDirection
    quantity: int
    unit_cost: Optional[Decimal]
    unit_price: Optional[Decimal]
    stock_before: int
    stock_after: int
    reason: Optional[str]
    reference_document: Optional[str]
    created_at: datetime
    product_id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True


class StockMovementDetail(StockMovementResponse):
    product_name: str = ""
    product_sku: str = ""
    user_name: Optional[str] = None

    class Config:
        from_attributes = True

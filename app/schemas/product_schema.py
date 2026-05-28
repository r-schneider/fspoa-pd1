from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

from app.enums.unit_measure_enum import UnitMeasure
from app.schemas.category_schema import CategoryResponse


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    barcode: Optional[str] = None
    sku: str
    minimum_stock: int = 0
    maximum_stock: Optional[int] = None
    price: Decimal
    cost_price: Optional[Decimal] = None
    unit_measure: UnitMeasure
    category_id: Optional[int] = None
    image_url: Optional[str] = None

    @field_validator("price", "cost_price", mode="before")
    @classmethod
    def price_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError("Preço não pode ser negativo")
        return v

    @field_validator("minimum_stock")
    @classmethod
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Estoque mínimo não pode ser negativo")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    minimum_stock: Optional[int] = None
    maximum_stock: Optional[int] = None
    price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    unit_measure: Optional[UnitMeasure] = None
    category_id: Optional[int] = None
    active: Optional[bool] = None
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    barcode: Optional[str]
    sku: str
    current_stock: int
    minimum_stock: int
    maximum_stock: Optional[int]
    price: Decimal
    cost_price: Optional[Decimal]
    unit_measure: UnitMeasure
    active: bool
    image_url: Optional[str]
    is_low_stock: bool
    is_out_of_stock: bool
    category_id: Optional[int]
    category: Optional[CategoryResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    name: str
    sku: str
    barcode: Optional[str]
    current_stock: int
    minimum_stock: int
    price: Decimal
    unit_measure: UnitMeasure
    active: bool
    is_low_stock: bool
    is_out_of_stock: bool
    category: Optional[CategoryResponse]

    class Config:
        from_attributes = True

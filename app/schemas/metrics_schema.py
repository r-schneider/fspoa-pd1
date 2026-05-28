from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    sku: str
    current_stock: int
    minimum_stock: int
    deficit: int

    class Config:
        from_attributes = True


class TopProductItem(BaseModel):
    product_id: int
    product_name: str
    sku: str
    total_quantity: int
    total_revenue: Optional[Decimal]


class DashboardMetrics(BaseModel):
    total_products: int
    active_products: int
    out_of_stock_count: int
    low_stock_count: int
    total_movements_today: int
    total_entries_today: int
    total_exits_today: int
    total_inventory_value: Decimal


class MovementSummary(BaseModel):
    date: str
    entries: int
    exits: int
    total_movements: int


class FullDashboard(BaseModel):
    metrics: DashboardMetrics
    low_stock_alerts: List[LowStockAlert]
    top_sold_products: List[TopProductItem]
    top_purchased_products: List[TopProductItem]
    recent_movements: List[dict]

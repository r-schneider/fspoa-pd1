from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_

from app.models.stock_movement_model import StockMovement
from app.enums.unit_measure_enum import MovementType, MovementDirection
from app.repositories.base_repository import BaseRepository


class StockMovementRepository(BaseRepository[StockMovement]):
    def __init__(self, db: Session):
        super().__init__(StockMovement, db)

    def get_by_product(self, product_id: int, skip: int = 0, limit: int = 50) -> List[StockMovement]:
        return (
            self.db.query(StockMovement)
            .filter(StockMovement.product_id == product_id)
            .order_by(desc(StockMovement.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_details(self, skip: int = 0, limit: int = 50, product_id: int = None,
                          movement_type: MovementType = None, start_date: datetime = None,
                          end_date: datetime = None) -> List[StockMovement]:
        q = (
            self.db.query(StockMovement)
            .options(joinedload(StockMovement.product), joinedload(StockMovement.user))
        )
        if product_id:
            q = q.filter(StockMovement.product_id == product_id)
        if movement_type:
            q = q.filter(StockMovement.movement_type == movement_type)
        if start_date:
            q = q.filter(StockMovement.created_at >= start_date)
        if end_date:
            q = q.filter(StockMovement.created_at <= end_date)
        return q.order_by(desc(StockMovement.created_at)).offset(skip).limit(limit).all()

    def count_today(self) -> int:
        today = date.today()
        return (
            self.db.query(StockMovement)
            .filter(func.date(StockMovement.created_at) == today)
            .count()
        )

    def count_today_by_direction(self, direction: MovementDirection) -> int:
        today = date.today()
        return (
            self.db.query(StockMovement)
            .filter(
                func.date(StockMovement.created_at) == today,
                StockMovement.direction == direction,
            )
            .count()
        )

    def top_sold_products(self, limit: int = 5) -> List[dict]:
        results = (
            self.db.query(
                StockMovement.product_id,
                func.sum(StockMovement.quantity).label("total_quantity"),
                func.sum(StockMovement.quantity * StockMovement.unit_price).label("total_revenue"),
            )
            .filter(StockMovement.movement_type == MovementType.SAIDA_VENDA)
            .group_by(StockMovement.product_id)
            .order_by(desc("total_quantity"))
            .limit(limit)
            .all()
        )
        return results

    def top_purchased_products(self, limit: int = 5) -> List:
        results = (
            self.db.query(
                StockMovement.product_id,
                func.sum(StockMovement.quantity).label("total_quantity"),
            )
            .filter(StockMovement.movement_type == MovementType.ENTRADA_COMPRA)
            .group_by(StockMovement.product_id)
            .order_by(desc("total_quantity"))
            .limit(limit)
            .all()
        )
        return results

    def movement_summary_by_day(self, days: int = 7) -> List:
        from sqlalchemy import cast, Date
        results = (
            self.db.query(
                cast(StockMovement.created_at, Date).label("day"),
                StockMovement.direction,
                func.count(StockMovement.id).label("count"),
            )
            .group_by("day", StockMovement.direction)
            .order_by(desc("day"))
            .limit(days * 2)
            .all()
        )
        return results

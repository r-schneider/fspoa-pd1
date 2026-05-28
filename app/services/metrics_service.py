from decimal import Decimal
from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.stock_movement_repository import StockMovementRepository
from app.enums.unit_measure_enum import MovementDirection
from app.schemas.metrics_schema import (
    DashboardMetrics, LowStockAlert, TopProductItem, FullDashboard
)


class MetricsService:
    def __init__(self, db: Session):
        self.product_repo = ProductRepository(db)
        self.movement_repo = StockMovementRepository(db)

    def get_dashboard_metrics(self) -> DashboardMetrics:
        total = self.product_repo.count()
        active = self.product_repo.count_active()
        out_of_stock = self.product_repo.count_out_of_stock()
        low_stock = self.product_repo.count_low_stock()

        movements_today = self.movement_repo.count_today()
        entries_today = self.movement_repo.count_today_by_direction(MovementDirection.ENTRADA)
        exits_today = self.movement_repo.count_today_by_direction(MovementDirection.SAIDA)

        # Total inventory value = sum(current_stock * price)
        products = self.product_repo.get_all(limit=99999)
        total_value = sum(
            (p.current_stock * (p.cost_price or p.price))
            for p in products
            if p.active and p.current_stock > 0
        )

        return DashboardMetrics(
            total_products=total,
            active_products=active,
            out_of_stock_count=out_of_stock,
            low_stock_count=low_stock,
            total_movements_today=movements_today,
            total_entries_today=entries_today,
            total_exits_today=exits_today,
            total_inventory_value=Decimal(str(round(total_value, 2))),
        )

    def get_low_stock_alerts(self):
        products = self.product_repo.get_low_stock_products()
        alerts = []
        for p in products:
            alerts.append(LowStockAlert(
                product_id=p.id,
                product_name=p.name,
                sku=p.sku,
                current_stock=p.current_stock,
                minimum_stock=p.minimum_stock,
                deficit=p.minimum_stock - p.current_stock,
            ))
        return alerts

    def get_top_sold_products(self, limit: int = 5):
        rows = self.movement_repo.top_sold_products(limit)
        result = []
        for row in rows:
            product = self.product_repo.get_by_id(row.product_id)
            if product:
                result.append(TopProductItem(
                    product_id=product.id,
                    product_name=product.name,
                    sku=product.sku,
                    total_quantity=row.total_quantity,
                    total_revenue=Decimal(str(round(row.total_revenue or 0, 2))),
                ))
        return result

    def get_top_purchased_products(self, limit: int = 5):
        rows = self.movement_repo.top_purchased_products(limit)
        result = []
        for row in rows:
            product = self.product_repo.get_by_id(row.product_id)
            if product:
                result.append(TopProductItem(
                    product_id=product.id,
                    product_name=product.name,
                    sku=product.sku,
                    total_quantity=row.total_quantity,
                    total_revenue=None,
                ))
        return result

    def get_full_dashboard(self) -> FullDashboard:
        metrics = self.get_dashboard_metrics()
        low_stock = self.get_low_stock_alerts()
        top_sold = self.get_top_sold_products()
        top_purchased = self.get_top_purchased_products()
        recent = self.movement_repo.get_with_details(skip=0, limit=10)

        recent_serialized = []
        for m in recent:
            recent_serialized.append({
                "id": m.id,
                "product_name": m.product.name if m.product else "",
                "movement_type": m.movement_type.value,
                "direction": m.direction.value,
                "quantity": m.quantity,
                "created_at": m.created_at.isoformat(),
            })

        return FullDashboard(
            metrics=metrics,
            low_stock_alerts=low_stock,
            top_sold_products=top_sold,
            top_purchased_products=top_purchased,
            recent_movements=recent_serialized,
        )

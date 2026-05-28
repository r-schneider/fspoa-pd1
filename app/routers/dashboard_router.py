from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.metrics_service import MetricsService
from app.schemas.metrics_schema import DashboardMetrics, LowStockAlert, TopProductItem, FullDashboard

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Métricas"])


@router.get("", response_model=FullDashboard)
def full_dashboard(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Retorna todos os dados do dashboard em uma única requisição"""
    return MetricsService(db).get_full_dashboard()


@router.get("/metrics", response_model=DashboardMetrics)
def get_metrics(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Retorna métricas gerais do estoque"""
    return MetricsService(db).get_dashboard_metrics()


@router.get("/alerts", response_model=List[LowStockAlert])
def get_alerts(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Alertas de produtos com estoque abaixo do mínimo"""
    return MetricsService(db).get_low_stock_alerts()


@router.get("/top-sold", response_model=List[TopProductItem])
def top_sold(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Produtos mais vendidos"""
    return MetricsService(db).get_top_sold_products(limit)


@router.get("/top-purchased", response_model=List[TopProductItem])
def top_purchased(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Produtos mais comprados/recebidos"""
    return MetricsService(db).get_top_purchased_products(limit)

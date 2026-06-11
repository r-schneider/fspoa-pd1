from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.services.metricas_service import MetricasService
from app.backend.schemas.metricas_schema import (
    MetricasDashboard, AlertaEstoqueBaixo, ProdutoRanking, DashboardCompleto,
    MovimentoPorDia, EstoquePorCategoria,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Métricas"])


@router.get("", response_model=DashboardCompleto)
def dashboard_completo(db: Session = Depends(get_db)):
    return MetricasService(db).dashboard_completo()


@router.get("/metricas", response_model=MetricasDashboard)
def metricas(db: Session = Depends(get_db)):
    return MetricasService(db).metricas_dashboard()


@router.get("/alertas", response_model=List[AlertaEstoqueBaixo])
def alertas(db: Session = Depends(get_db)):
    return MetricasService(db).alertas_estoque_baixo()


@router.get("/mais-vendidos", response_model=List[ProdutoRanking])
def mais_vendidos(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    return MetricasService(db).mais_vendidos(limit)


@router.get("/mais-comprados", response_model=List[ProdutoRanking])
def mais_comprados(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    return MetricasService(db).mais_comprados(limit)


@router.get("/movimentos-por-dia", response_model=List[MovimentoPorDia])
def movimentos_por_dia(dias: int = Query(7, ge=1, le=90), db: Session = Depends(get_db)):
    return MetricasService(db).movimentos_por_dia(dias)


@router.get("/estoque-por-categoria", response_model=List[EstoquePorCategoria])
def estoque_por_categoria(db: Session = Depends(get_db)):
    return MetricasService(db).estoque_por_categoria()

from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class AlertaEstoqueBaixo(BaseModel):
    produto_id: int
    nome_produto: str
    sku: str
    estoque_atual: int
    estoque_minimo: int
    deficit: int

    class Config:
        from_attributes = True


class ProdutoRanking(BaseModel):
    produto_id: int
    nome_produto: str
    sku: str
    quantidade_total: int
    receita_total: Optional[Decimal]


class MetricasDashboard(BaseModel):
    total_produtos: int
    produtos_ativos: int
    sem_estoque: int
    estoque_baixo: int
    movimentacoes_hoje: int
    entradas_hoje: int
    saidas_hoje: int
    valor_inventario: Decimal


class ResumoMovimentacao(BaseModel):
    data: str
    entradas: int
    saidas: int
    total: int


class MovimentoPorDia(BaseModel):
    data: str
    entradas: int
    saidas: int


class EstoquePorCategoria(BaseModel):
    categoria: str
    total_produtos: int
    valor_total: float


class DashboardCompleto(BaseModel):
    metricas: MetricasDashboard
    alertas_estoque: List[AlertaEstoqueBaixo]
    mais_vendidos: List[ProdutoRanking]
    mais_comprados: List[ProdutoRanking]
    movimentacoes_recentes: List[dict]

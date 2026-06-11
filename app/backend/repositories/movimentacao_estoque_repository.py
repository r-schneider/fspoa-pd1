from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc

from app.backend.models.movimentacao_estoque_model import MovimentacaoEstoque
from app.backend.enums.estoque_enum import TipoMovimentacao, DirecaoMovimentacao
from app.backend.repositories.base_repository import BaseRepository


class MovimentacaoEstoqueRepository(BaseRepository[MovimentacaoEstoque]):
    def __init__(self, db: Session):
        super().__init__(MovimentacaoEstoque, db)

    def buscar_por_produto(self, produto_id: int, skip: int = 0, limit: int = 50) -> List[MovimentacaoEstoque]:
        return (
            self.db.query(MovimentacaoEstoque)
            .filter(MovimentacaoEstoque.produto_id == produto_id)
            .order_by(desc(MovimentacaoEstoque.criado_em))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_com_detalhes(
        self,
        skip: int = 0,
        limit: int = 50,
        produto_id: int = None,
        tipo_movimentacao: TipoMovimentacao = None,
        data_inicio: datetime = None,
        data_fim: datetime = None,
    ) -> List[MovimentacaoEstoque]:
        q = (
            self.db.query(MovimentacaoEstoque)
            .options(joinedload(MovimentacaoEstoque.produto), joinedload(MovimentacaoEstoque.fornecedor))
        )
        if produto_id:
            q = q.filter(MovimentacaoEstoque.produto_id == produto_id)
        if tipo_movimentacao:
            q = q.filter(MovimentacaoEstoque.tipo_movimentacao == tipo_movimentacao)
        if data_inicio:
            q = q.filter(MovimentacaoEstoque.criado_em >= data_inicio)
        if data_fim:
            q = q.filter(MovimentacaoEstoque.criado_em <= data_fim)
        return q.order_by(desc(MovimentacaoEstoque.criado_em)).offset(skip).limit(limit).all()

    def contar_hoje(self) -> int:
        hoje = date.today()
        return (
            self.db.query(MovimentacaoEstoque)
            .filter(func.date(MovimentacaoEstoque.criado_em) == hoje)
            .count()
        )

    def contar_hoje_por_direcao(self, direcao: DirecaoMovimentacao) -> int:
        hoje = date.today()
        return (
            self.db.query(MovimentacaoEstoque)
            .filter(
                func.date(MovimentacaoEstoque.criado_em) == hoje,
                MovimentacaoEstoque.direcao == direcao,
            )
            .count()
        )

    def mais_vendidos(self, limit: int = 5) -> List:
        return (
            self.db.query(
                MovimentacaoEstoque.produto_id,
                func.sum(MovimentacaoEstoque.quantidade).label("quantidade_total"),
                func.sum(MovimentacaoEstoque.quantidade * MovimentacaoEstoque.preco_unitario).label("receita_total"),
            )
            .filter(MovimentacaoEstoque.tipo_movimentacao == TipoMovimentacao.SAIDA_VENDA)
            .group_by(MovimentacaoEstoque.produto_id)
            .order_by(desc("quantidade_total"))
            .limit(limit)
            .all()
        )

    def mais_comprados(self, limit: int = 5) -> List:
        return (
            self.db.query(
                MovimentacaoEstoque.produto_id,
                func.sum(MovimentacaoEstoque.quantidade).label("quantidade_total"),
            )
            .filter(MovimentacaoEstoque.tipo_movimentacao == TipoMovimentacao.ENTRADA_COMPRA)
            .group_by(MovimentacaoEstoque.produto_id)
            .order_by(desc("quantidade_total"))
            .limit(limit)
            .all()
        )

    def resumo_por_dia(self, dias: int = 7) -> List:
        from sqlalchemy import cast, Date
        return (
            self.db.query(
                cast(MovimentacaoEstoque.criado_em, Date).label("dia"),
                MovimentacaoEstoque.direcao,
                func.count(MovimentacaoEstoque.id).label("contagem"),
            )
            .group_by("dia", MovimentacaoEstoque.direcao)
            .order_by(desc("dia"))
            .limit(dias * 2)
            .all()
        )

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

from app.backend.enums.estoque_enum import TipoMovimentacao, DirecaoMovimentacao


class EntradaEstoqueCriar(BaseModel):
    produto_id: int
    tipo_movimentacao: TipoMovimentacao
    quantidade: int
    custo_unitario: Optional[Decimal] = None
    motivo: Optional[str] = None
    documento_referencia: Optional[str] = None
    fornecedor_id: Optional[int] = None

    @field_validator("tipo_movimentacao")
    @classmethod
    def deve_ser_entrada(cls, v):
        if v not in (TipoMovimentacao.ENTRADA_COMPRA, TipoMovimentacao.ENTRADA_AJUSTE, TipoMovimentacao.ENTRADA_DEVOLUCAO):
            raise ValueError("Use SaidaEstoqueCriar para saídas de estoque")
        return v

    @field_validator("quantidade")
    @classmethod
    def quantidade_positiva(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class SaidaEstoqueCriar(BaseModel):
    produto_id: int
    tipo_movimentacao: TipoMovimentacao
    quantidade: int
    preco_unitario: Optional[Decimal] = None
    motivo: Optional[str] = None
    documento_referencia: Optional[str] = None

    @field_validator("tipo_movimentacao")
    @classmethod
    def deve_ser_saida(cls, v):
        if v not in (TipoMovimentacao.SAIDA_VENDA, TipoMovimentacao.SAIDA_BAIXA, TipoMovimentacao.SAIDA_AJUSTE):
            raise ValueError("Use EntradaEstoqueCriar para entradas de estoque")
        return v

    @field_validator("quantidade")
    @classmethod
    def quantidade_positiva(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        return v


class MovimentacaoEstoqueResposta(BaseModel):
    id: int
    tipo_movimentacao: TipoMovimentacao
    direcao: DirecaoMovimentacao
    quantidade: int
    custo_unitario: Optional[Decimal]
    preco_unitario: Optional[Decimal]
    estoque_antes: int
    estoque_depois: int
    motivo: Optional[str]
    documento_referencia: Optional[str]
    criado_em: datetime
    produto_id: int
    fornecedor_id: Optional[int]

    class Config:
        from_attributes = True


class MovimentacaoEstoqueDetalhe(MovimentacaoEstoqueResposta):
    nome_produto: str = ""
    sku_produto: str = ""
    nome_fornecedor: Optional[str] = None

    class Config:
        from_attributes = True

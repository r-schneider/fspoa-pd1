from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.core.database import BaseDados
from app.backend.enums.estoque_enum import TipoMovimentacao, DirecaoMovimentacao


class MovimentacaoEstoque(BaseDados):
    __tablename__ = "MOVIMENTACOES_ESTOQUE"

    id = Column("ID", Integer, primary_key=True, index=True)
    tipo_movimentacao = Column("TIPO_MOVIMENTACAO", SqlEnum(TipoMovimentacao), nullable=False)
    direcao = Column("DIRECAO", SqlEnum(DirecaoMovimentacao), nullable=False)
    quantidade = Column("QUANTIDADE", Integer, nullable=False)
    custo_unitario = Column("CUSTO_UNITARIO", Numeric(10, 2), nullable=True)
    preco_unitario = Column("PRECO_UNITARIO", Numeric(10, 2), nullable=True)
    estoque_antes = Column("ESTOQUE_ANTES", Integer, nullable=False)
    estoque_depois = Column("ESTOQUE_DEPOIS", Integer, nullable=False)
    motivo = Column("MOTIVO", Text, nullable=True)
    documento_referencia = Column("DOCUMENTO_REFERENCIA", String(100), nullable=True)
    criado_em = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow, index=True)

    produto_id = Column("ID_PRODUTO", Integer, ForeignKey("PRODUTOS.ID"), nullable=False)
    fornecedor_id = Column("ID_FORNECEDOR", Integer, ForeignKey("FORNECEDORES.ID"), nullable=True)

    produto = relationship("Produto", back_populates="movimentacoes")
    fornecedor = relationship("Fornecedor", back_populates="movimentacoes")

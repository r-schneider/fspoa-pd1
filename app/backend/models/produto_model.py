from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.core.database import BaseDados
from app.backend.enums.estoque_enum import UnidadeMedida


class Produto(BaseDados):
    __tablename__ = "PRODUTOS"

    id = Column("ID", Integer, primary_key=True, index=True)
    nome = Column("NOME", String(200), nullable=False)
    descricao = Column("DESCRICAO", Text, nullable=True)
    codigo_barras = Column("CODIGO_BARRAS", String(50), unique=True, nullable=True)
    sku = Column("SKU", String(50), unique=True, nullable=False)
    estoque_atual = Column("ESTOQUE_ATUAL", Integer, nullable=False, default=0)
    estoque_minimo = Column("ESTOQUE_MINIMO", Integer, nullable=False, default=0)
    estoque_maximo = Column("ESTOQUE_MAXIMO", Integer, nullable=True)
    preco = Column("PRECO_VENDA", Numeric(10, 2), nullable=False)
    preco_custo = Column("PRECO_CUSTO", Numeric(10, 2), nullable=True)
    unidade_medida = Column("UNIDADE_MEDIDA", SqlEnum(UnidadeMedida), nullable=False)
    ativo = Column("ATIVO", Boolean, default=True)
    url_imagem = Column("URL_IMAGEM", String(500), nullable=True)
    criado_em = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    atualizado_em = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categoria_id = Column("ID_CATEGORIA", Integer, ForeignKey("CATEGORIAS.ID"), nullable=True)
    categoria = relationship("Categoria", back_populates="produtos")
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")

    @property
    def estoque_baixo(self) -> bool:
        return self.estoque_atual <= self.estoque_minimo

    @property
    def sem_estoque(self) -> bool:
        return self.estoque_atual == 0

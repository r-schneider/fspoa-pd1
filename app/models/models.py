from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, Enum as SqlEnum
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.enums.unit_measure_enum import UnitMeasure


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    lugar = Column(String(100))

    produtos = relationship("Produto", back_populates="categoria")


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)
    email = Column(String(150))
    telefone = Column(String(20))
    endereco = Column(String(250))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    codigo_barra = Column(String(50), unique=True)
    sku = Column(String(50), unique=True)
    estoque_atual = Column(Integer, nullable=False, default=0)
    estoque_minimo = Column(Integer, nullable=False, default=0)
    preco_compra = Column(Float, nullable=False, default=0.0)
    preco_venda = Column(Float, nullable=False, default=0.0)
    unidade_medida = Column(SqlEnum(UnitMeasure), nullable=False, default=UnitMeasure.UNIT)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="produtos")

    movimentos = relationship("MovimentoEstoque", back_populates="produto")


class MovimentoEstoque(Base):
    __tablename__ = "movimentos_estoque"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(20), nullable=False)        # "ENTRADA" | "SAIDA"
    motivo = Column(String(50), nullable=False)      # ex: "Venda", "Perda", "Compra"
    quantidade = Column(Integer, nullable=False)
    responsavel = Column(String(100))
    observacoes = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    produto = relationship("Produto", back_populates="movimentos")

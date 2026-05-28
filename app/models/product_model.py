from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.enums.unit_measure_enum import UnitMeasure


class Product(Base):
    __tablename__ = "PRODUTOS"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("NOME", String(200), nullable=False)
    description = Column("DESCRICAO", Text, nullable=True)
    barcode = Column("CODIGO_BARRAS", String(50), unique=True, nullable=True)
    sku = Column("SKU", String(50), unique=True, nullable=False)
    current_stock = Column("ESTOQUE_ATUAL", Integer, nullable=False, default=0)
    minimum_stock = Column("ESTOQUE_MINIMO", Integer, nullable=False, default=0)
    maximum_stock = Column("ESTOQUE_MAXIMO", Integer, nullable=True)
    price = Column("PRECO_VENDA", Numeric(10, 2), nullable=False)
    cost_price = Column("PRECO_CUSTO", Numeric(10, 2), nullable=True)
    unit_measure = Column("UNIDADE_MEDIDA", SqlEnum(UnitMeasure), nullable=False)
    active = Column("ATIVO", Boolean, default=True)
    image_url = Column("URL_IMAGEM", String(500), nullable=True)
    created_at = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    updated_at = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = Column("ID_CATEGORIA", Integer, ForeignKey("CATEGORIAS.ID"), nullable=True)
    category = relationship("Category", back_populates="products")
    movements = relationship("StockMovement", back_populates="product")

    @property
    def is_low_stock(self) -> bool:
        return self.current_stock <= self.minimum_stock

    @property
    def is_out_of_stock(self) -> bool:
        return self.current_stock == 0

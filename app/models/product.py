from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Enum as SqlEnum
from app.core.database import Base
from app.enums.unit_measure_enum import UnitMeasure

class Product(Base):
    __tablename__ = "PRODUTOS"

    id = Column("ID", Integer, primary_key=True, index=True)  
    name = Column("NOME", String, nullable=False)
    description = Column("DESCRICAO", String)  
    barcode = Column("CODIGO_BARRAS", String, unique=True)
    sku = Column("SKU", String, unique=True)  
    current_stock = Column("ESTOQUE_ATUAL", Integer, nullable=False, default=0) 
    minimum_stock = Column("ESTOQUE_MINIMO", Integer, nullable=False, default=0)  
    price  = Column("PRECO", Numeric(10,2), nullable=False)
    unit_measure = Column("UNIDADE_MEDIDA", SqlEnum(UnitMeasure), nullable=False)
    active = Column("ATIVO", Boolean, default=True)  
    created_at = ("DATA_CRIACAO", DateTime)
    updated_at = ("DATA_ATUALIZACAO", DateTime)
    category_id = Column("ID_CATEGORIA", Integer)
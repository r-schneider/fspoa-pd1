from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Enum as SqlEnum
from app.core.database import Base
from app.enums.unit_measure_enum import UnitMeasure

class Product(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)  
    nome = Column(String, nullable=False)
    descricao = Column(String)  
    codigo_barras = Column(String, unique=True)
    sku = Column(String, unique=True)  
    estoque_atual = Column(Integer, nullable=False, default=0) 
    estoque_minimo = Column(Integer, nullable=False, default=0)  
    valor_venda  = Column(Numeric(10,2), nullable=False)
    marca = Column(String)
    unidade_medida = Column(SqlEnum(UnitMeasure), nullable=False)
    ativo = Column(Boolean, default=True)  
    criado_em = (DateTime)
    atualizado_em = (DateTime)
    categoria_id = Column(Integer)
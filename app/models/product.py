from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Product(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)  
    nome = Column(String)  
    codigo_barra = Column(String)  
    estoque_atual = Column(Integer) 
    estoque_minimo = Column(Integer)  
    preco_compra = Column(Float)  
    preco_venda  = Column(Float)  
    categoria_id = Column(Integer)  
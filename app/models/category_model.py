from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Category(Base):
    __tablename__ = "CATEGORIAS"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("NOME", String(100), nullable=False, unique=True)
    description = Column("DESCRICAO", Text, nullable=True)
    active = Column("ATIVO", Boolean, default=True)
    created_at = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    updated_at = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")

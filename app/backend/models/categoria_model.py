from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.core.database import BaseDados


class Categoria(BaseDados):
    __tablename__ = "CATEGORIAS"

    id = Column("ID", Integer, primary_key=True, index=True)
    nome = Column("NOME", String(100), nullable=False, unique=True)
    descricao = Column("DESCRICAO", Text, nullable=True)
    ativo = Column("ATIVO", Boolean, default=True)
    criado_em = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    atualizado_em = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    produtos = relationship("Produto", back_populates="categoria")

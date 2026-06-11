from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.core.database import BaseDados


class Fornecedor(BaseDados):
    __tablename__ = "FORNECEDORES"

    id = Column("ID", Integer, primary_key=True, index=True)
    nome = Column("NOME", String(200), nullable=False)
    cnpj = Column("CNPJ", String(18), unique=True, nullable=True)
    telefone = Column("TELEFONE", String(20), nullable=True)
    email = Column("EMAIL", String(254), nullable=True)
    endereco = Column("ENDERECO", String(500), nullable=True)
    ativo = Column("ATIVO", Boolean, default=True)
    criado_em = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    atualizado_em = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movimentacoes = relationship("MovimentacaoEstoque", back_populates="fornecedor")

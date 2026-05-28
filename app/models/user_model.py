from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class User(Base):
    __tablename__ = "USUARIOS"

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("NOME", String, nullable=False)
    email = Column("EMAIL", String, unique=True, nullable=False, index=True)
    hashed_password = Column("SENHA_HASH", String, nullable=False)
    active = Column("ATIVO", Boolean, default=True)
    created_at = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow)
    updated_at = Column("DATA_ATUALIZACAO", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movements = relationship("StockMovement", back_populates="user")

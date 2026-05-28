from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.enums.unit_measure_enum import MovementType, MovementDirection


class StockMovement(Base):
    __tablename__ = "MOVIMENTACOES_ESTOQUE"

    id = Column("ID", Integer, primary_key=True, index=True)
    movement_type = Column("TIPO_MOVIMENTACAO", SqlEnum(MovementType), nullable=False)
    direction = Column("DIRECAO", SqlEnum(MovementDirection), nullable=False)
    quantity = Column("QUANTIDADE", Integer, nullable=False)
    unit_cost = Column("CUSTO_UNITARIO", Numeric(10, 2), nullable=True)   # custo na compra
    unit_price = Column("PRECO_UNITARIO", Numeric(10, 2), nullable=True)  # preço na venda
    stock_before = Column("ESTOQUE_ANTES", Integer, nullable=False)
    stock_after = Column("ESTOQUE_DEPOIS", Integer, nullable=False)
    reason = Column("MOTIVO", Text, nullable=True)
    reference_document = Column("DOCUMENTO_REFERENCIA", String(100), nullable=True)  # NF, pedido etc.
    created_at = Column("DATA_CRIACAO", DateTime, default=datetime.utcnow, index=True)

    product_id = Column("ID_PRODUTO", Integer, ForeignKey("PRODUTOS.ID"), nullable=False)
    user_id = Column("ID_USUARIO", Integer, ForeignKey("USUARIOS.ID"), nullable=True)

    product = relationship("Product", back_populates="movements")
    user = relationship("User", back_populates="movements")

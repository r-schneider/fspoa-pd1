from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.stock_movement_model import StockMovement
from app.models.user_model import User
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_movement_repository import StockMovementRepository
from app.enums.unit_measure_enum import MovementType, MovementDirection
from app.schemas.stock_movement_schema import StockEntryCreate, StockExitCreate, StockMovementDetail


# Maps each movement type to its direction
MOVEMENT_DIRECTION_MAP = {
    MovementType.ENTRADA_COMPRA: MovementDirection.ENTRADA,
    MovementType.ENTRADA_AJUSTE: MovementDirection.ENTRADA,
    MovementType.ENTRADA_DEVOLUCAO: MovementDirection.ENTRADA,
    MovementType.SAIDA_VENDA: MovementDirection.SAIDA,
    MovementType.SAIDA_BAIXA: MovementDirection.SAIDA,
    MovementType.SAIDA_AJUSTE: MovementDirection.SAIDA,
}


class StockMovementService:
    def __init__(self, db: Session):
        self.repo = StockMovementRepository(db)
        self.product_repo = ProductRepository(db)

    def register_entry(self, data: StockEntryCreate, current_user: User) -> StockMovement:
        product = self.product_repo.get_by_id(data.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        if not product.active:
            raise HTTPException(status_code=400, detail="Produto inativo não pode receber movimentações")

        stock_before = product.current_stock
        product.current_stock += data.quantity

        movement = StockMovement(
            product_id=product.id,
            user_id=current_user.id,
            movement_type=data.movement_type,
            direction=MovementDirection.ENTRADA,
            quantity=data.quantity,
            unit_cost=data.unit_cost,
            stock_before=stock_before,
            stock_after=product.current_stock,
            reason=data.reason,
            reference_document=data.reference_document,
        )

        # Update cost price if provided
        if data.unit_cost:
            product.cost_price = data.unit_cost

        self.product_repo.update(product)
        return self.repo.create(movement)

    def register_exit(self, data: StockExitCreate, current_user: User) -> StockMovement:
        product = self.product_repo.get_by_id(data.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        if not product.active:
            raise HTTPException(status_code=400, detail="Produto inativo não pode receber movimentações")
        if product.current_stock < data.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente. Disponível: {product.current_stock}, Solicitado: {data.quantity}"
            )

        stock_before = product.current_stock
        product.current_stock -= data.quantity

        movement = StockMovement(
            product_id=product.id,
            user_id=current_user.id,
            movement_type=data.movement_type,
            direction=MovementDirection.SAIDA,
            quantity=data.quantity,
            unit_price=data.unit_price,
            stock_before=stock_before,
            stock_after=product.current_stock,
            reason=data.reason,
            reference_document=data.reference_document,
        )

        self.product_repo.update(product)
        return self.repo.create(movement)

    def get_history(
        self,
        product_id: int = None,
        movement_type: MovementType = None,
        start_date: datetime = None,
        end_date: datetime = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[StockMovementDetail]:
        movements = self.repo.get_with_details(skip, limit, product_id, movement_type, start_date, end_date)
        result = []
        for m in movements:
            item = StockMovementDetail.model_validate(m)
            item.product_name = m.product.name if m.product else ""
            item.product_sku = m.product.sku if m.product else ""
            item.user_name = m.user.name if m.user else None
            result.append(item)
        return result

    def get_product_history(self, product_id: int, skip: int = 0, limit: int = 50) -> List[StockMovement]:
        # Validate product exists
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self.repo.get_by_product(product_id, skip, limit)

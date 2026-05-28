from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models.product_model import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_by_id_with_category(self, product_id: int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.barcode == barcode).first()

    def search(
        self,
        query: str = None,
        category_id: int = None,
        active: bool = None,
        low_stock: bool = False,
        out_of_stock: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        q = self.db.query(Product).options(joinedload(Product.category))

        if query:
            q = q.filter(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%"),
                    Product.barcode.ilike(f"%{query}%"),
                )
            )
        if category_id is not None:
            q = q.filter(Product.category_id == category_id)
        if active is not None:
            q = q.filter(Product.active == active)
        if out_of_stock:
            q = q.filter(Product.current_stock == 0)
        elif low_stock:
            q = q.filter(Product.current_stock <= Product.minimum_stock)

        return q.order_by(Product.name).offset(skip).limit(limit).all()

    def get_low_stock_products(self) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.active == True, Product.current_stock <= Product.minimum_stock)
            .order_by(Product.current_stock)
            .all()
        )

    def sku_exists(self, sku: str, exclude_id: int = None) -> bool:
        query = self.db.query(Product).filter(Product.sku == sku)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        return query.first() is not None

    def barcode_exists(self, barcode: str, exclude_id: int = None) -> bool:
        if not barcode:
            return False
        query = self.db.query(Product).filter(Product.barcode == barcode)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        return query.first() is not None

    def count_active(self) -> int:
        return self.db.query(Product).filter(Product.active == True).count()

    def count_out_of_stock(self) -> int:
        return self.db.query(Product).filter(Product.active == True, Product.current_stock == 0).count()

    def count_low_stock(self) -> int:
        return (
            self.db.query(Product)
            .filter(Product.active == True, Product.current_stock <= Product.minimum_stock, Product.current_stock > 0)
            .count()
        )

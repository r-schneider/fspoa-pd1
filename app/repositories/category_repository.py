from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.category_model import Category
from app.models.product_model import Product
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all_active(self) -> List[Category]:
        return self.db.query(Category).filter(Category.active == True).all()

    def get_with_product_count(self):
        return (
            self.db.query(Category, func.count(Product.id).label("product_count"))
            .outerjoin(Product, (Product.category_id == Category.id) & (Product.active == True))
            .group_by(Category.id)
            .all()
        )

    def name_exists(self, name: str, exclude_id: int = None) -> bool:
        query = self.db.query(Category).filter(Category.name == name)
        if exclude_id:
            query = query.filter(Category.id != exclude_id)
        return query.first() is not None

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryWithCount


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create(self, data: CategoryCreate) -> Category:
        if self.repo.name_exists(data.name):
            raise HTTPException(status_code=409, detail="Categoria com este nome já existe")
        category = Category(name=data.name, description=data.description)
        return self.repo.create(category)

    def get_by_id(self, category_id: int) -> Category:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return category

    def get_all(self, active_only: bool = False) -> List[Category]:
        if active_only:
            return self.repo.get_all_active()
        return self.repo.get_all()

    def get_all_with_count(self) -> List[CategoryWithCount]:
        rows = self.repo.get_with_product_count()
        result = []
        for category, count in rows:
            item = CategoryWithCount.model_validate(category)
            item.product_count = count
            result.append(item)
        return result

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.get_by_id(category_id)
        if data.name and self.repo.name_exists(data.name, exclude_id=category_id):
            raise HTTPException(status_code=409, detail="Categoria com este nome já existe")
        if data.name is not None:
            category.name = data.name
        if data.description is not None:
            category.description = data.description
        if data.active is not None:
            category.active = data.active
        return self.repo.update(category)

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        if category.products:
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir categoria com produtos associados. Desative-a ou realoque os produtos."
            )
        self.repo.delete(category)

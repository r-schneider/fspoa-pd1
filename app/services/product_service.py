from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.cat_repo = CategoryRepository(db)

    def create(self, data: ProductCreate) -> Product:
        if self.repo.sku_exists(data.sku):
            raise HTTPException(status_code=409, detail=f"SKU '{data.sku}' já cadastrado")
        if data.barcode and self.repo.barcode_exists(data.barcode):
            raise HTTPException(status_code=409, detail=f"Código de barras '{data.barcode}' já cadastrado")
        if data.category_id:
            cat = self.cat_repo.get_by_id(data.category_id)
            if not cat:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

        product = Product(**data.model_dump())
        return self.repo.create(product)

    def get_by_id(self, product_id: int) -> Product:
        product = self.repo.get_by_id_with_category(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return product

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
        return self.repo.search(query, category_id, active, low_stock, out_of_stock, skip, limit)

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_by_id(product_id)

        if data.sku and self.repo.sku_exists(data.sku, exclude_id=product_id):
            raise HTTPException(status_code=409, detail=f"SKU '{data.sku}' já em uso")
        if data.barcode and self.repo.barcode_exists(data.barcode, exclude_id=product_id):
            raise HTTPException(status_code=409, detail=f"Código de barras já em uso")
        if data.category_id:
            cat = self.cat_repo.get_by_id(data.category_id)
            if not cat:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)

        return self.repo.update(product)

    def delete(self, product_id: int) -> None:
        product = self.get_by_id(product_id)
        if product.movements:
            raise HTTPException(
                status_code=409,
                detail="Produto possui movimentações. Desative-o em vez de excluir."
            )
        self.repo.delete(product)

    def get_low_stock_alerts(self) -> List[Product]:
        return self.repo.get_low_stock_products()

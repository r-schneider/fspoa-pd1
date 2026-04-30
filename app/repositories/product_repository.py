from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:

    def create(self, db: Session, nome: str):
        product = Product(nome = nome)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    def find_all(self, db: Session):
        return db.query(Product).all()
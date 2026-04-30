from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.database import Base, engine, SessionLocal
from app.repositories.product_repository import ProductRepository

app = FastAPI()
repository = ProductRepository()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return repository.find_all(db)

@app.post("/products")
def create_product(nome: str, db: Session = Depends(get_db)):
    return repository.create(db, nome)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.database import Base, engine, SessionLocal
from app.repositories.product_repository import ProductRepository
from app.routers import fornecedor_router, saida_router

app = FastAPI(
    title="StockMaster API",
    description="Backend do sistema de controle de estoque para ferragem.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fornecedor_router.router)
app.include_router(saida_router.router)

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
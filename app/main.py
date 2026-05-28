from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.routers import auth_router, category_router, product_router, stock_router, dashboard_router

# Import all models so SQLAlchemy registers them before create_all
import app.models  # noqa: F401

app = FastAPI(
    title="Ferragem Pro — API",
    description="Sistema de Gestão de Estoque para Ferragens",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(stock_router)
app.include_router(dashboard_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "Ferragem Pro API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

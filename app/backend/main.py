from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.backend.core.database import engine, BaseDados
from app.backend.routers import categoria_router, produto_router, estoque_router, dashboard_router, fornecedor_router

import app.backend.models  # noqa: F401

app = FastAPI(
    title="Stockmaster — API",
    description="Sistema de Gestão de Estoque para Ferragens",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(produto_router)
app.include_router(estoque_router)
app.include_router(dashboard_router)
app.include_router(fornecedor_router)


@app.get("/", tags=["Health"])
def raiz():
    return {"status": "ok", "app": "Stockmaster API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

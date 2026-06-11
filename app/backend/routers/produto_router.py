from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.services.produto_service import ProdutoService
from app.backend.schemas.produto_schema import ProdutoCriar, ProdutoAtualizar, ProdutoResposta, ProdutoListaResposta
from app.backend.schemas.metricas_schema import AlertaEstoqueBaixo

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResposta, status_code=201)
def criar_produto(data: ProdutoCriar, db: Session = Depends(get_db)):
    return ProdutoService(db).criar(data)


@router.get("", response_model=List[ProdutoListaResposta])
def listar_produtos(
    q: Optional[str] = Query(None, description="Busca por nome, SKU ou código de barras"),
    categoria_id: Optional[int] = Query(None),
    ativo: Optional[bool] = Query(None),
    estoque_baixo: bool = Query(False),
    sem_estoque: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return ProdutoService(db).pesquisar(q, categoria_id, ativo, estoque_baixo, sem_estoque, skip, limit)


@router.get("/estoque-baixo", response_model=List[AlertaEstoqueBaixo])
def alertas_estoque_baixo(db: Session = Depends(get_db)):
    produtos = ProdutoService(db).alertas_estoque_baixo()
    return [
        AlertaEstoqueBaixo(
            produto_id=p.id,
            nome_produto=p.nome,
            sku=p.sku,
            estoque_atual=p.estoque_atual,
            estoque_minimo=p.estoque_minimo,
            deficit=p.estoque_minimo - p.estoque_atual,
        )
        for p in produtos
    ]


@router.get("/{produto_id}", response_model=ProdutoResposta)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    return ProdutoService(db).buscar_por_id(produto_id)


@router.put("/{produto_id}", response_model=ProdutoResposta)
def atualizar_produto(produto_id: int, data: ProdutoAtualizar, db: Session = Depends(get_db)):
    return ProdutoService(db).atualizar(produto_id, data)


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    ProdutoService(db).deletar(produto_id)

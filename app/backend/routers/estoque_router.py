from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.services.movimentacao_estoque_service import MovimentacaoEstoqueService
from app.backend.schemas.movimentacao_estoque_schema import (
    EntradaEstoqueCriar, SaidaEstoqueCriar, MovimentacaoEstoqueResposta, MovimentacaoEstoqueDetalhe
)
from app.backend.enums.estoque_enum import TipoMovimentacao

router = APIRouter(prefix="/estoque", tags=["Movimentações de Estoque"])


@router.post("/entrada", response_model=MovimentacaoEstoqueResposta, status_code=201)
def registrar_entrada(data: EntradaEstoqueCriar, db: Session = Depends(get_db)):
    return MovimentacaoEstoqueService(db).registrar_entrada(data)


@router.post("/saida", response_model=MovimentacaoEstoqueResposta, status_code=201)
def registrar_saida(data: SaidaEstoqueCriar, db: Session = Depends(get_db)):
    return MovimentacaoEstoqueService(db).registrar_saida(data)


@router.get("/historico", response_model=List[MovimentacaoEstoqueDetalhe])
def historico_movimentacoes(
    produto_id: Optional[int] = Query(None),
    tipo_movimentacao: Optional[TipoMovimentacao] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return MovimentacaoEstoqueService(db).buscar_historico(
        produto_id, tipo_movimentacao, data_inicio, data_fim, skip, limit
    )


@router.get("/historico/{produto_id}", response_model=List[MovimentacaoEstoqueResposta])
def historico_produto(
    produto_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return MovimentacaoEstoqueService(db).buscar_historico_produto(produto_id, skip, limit)

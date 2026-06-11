from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.services.fornecedor_service import FornecedorService
from app.backend.schemas.fornecedor_schema import FornecedorCriar, FornecedorAtualizar, FornecedorResposta

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])


@router.post("", response_model=FornecedorResposta, status_code=201)
def criar_fornecedor(data: FornecedorCriar, db: Session = Depends(get_db)):
    return FornecedorService(db).criar(data)


@router.get("", response_model=List[FornecedorResposta])
def listar_fornecedores(somente_ativos: bool = Query(False), db: Session = Depends(get_db)):
    return FornecedorService(db).buscar_todos(somente_ativos)


@router.get("/{fornecedor_id}", response_model=FornecedorResposta)
def buscar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    return FornecedorService(db).buscar_por_id(fornecedor_id)


@router.put("/{fornecedor_id}", response_model=FornecedorResposta)
def atualizar_fornecedor(fornecedor_id: int, data: FornecedorAtualizar, db: Session = Depends(get_db)):
    return FornecedorService(db).atualizar(fornecedor_id, data)


@router.delete("/{fornecedor_id}", status_code=204)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    FornecedorService(db).deletar(fornecedor_id)

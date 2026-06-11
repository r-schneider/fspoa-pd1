from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.services.categoria_service import CategoriaService
from app.backend.schemas.categoria_schema import CategoriaCriar, CategoriaAtualizar, CategoriaResposta, CategoriaComContagem

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("", response_model=CategoriaResposta, status_code=201)
def criar_categoria(data: CategoriaCriar, db: Session = Depends(get_db)):
    return CategoriaService(db).criar(data)


@router.get("", response_model=List[CategoriaComContagem])
def listar_categorias(somente_ativos: bool = Query(False), db: Session = Depends(get_db)):
    return CategoriaService(db).buscar_todos_com_contagem()


@router.get("/{categoria_id}", response_model=CategoriaResposta)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return CategoriaService(db).buscar_por_id(categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaResposta)
def atualizar_categoria(categoria_id: int, data: CategoriaAtualizar, db: Session = Depends(get_db)):
    return CategoriaService(db).atualizar(categoria_id, data)


@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    CategoriaService(db).deletar(categoria_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import FornecedorCreate, FornecedorUpdate, FornecedorResponse
import app.services.fornecedor_service as service

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])


@router.post("/", response_model=FornecedorResponse, status_code=201)
def criar(data: FornecedorCreate, db: Session = Depends(get_db)):
    """Cadastra um novo fornecedor."""
    return service.criar_fornecedor(db, data)


@router.get("/", response_model=list[FornecedorResponse])
def listar(db: Session = Depends(get_db)):
    """Lista todos os fornecedores ativos."""
    return service.listar_fornecedores(db)


@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def buscar(fornecedor_id: int, db: Session = Depends(get_db)):
    """Busca fornecedor por ID."""
    return service.buscar_fornecedor(db, fornecedor_id)


@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar(fornecedor_id: int, data: FornecedorUpdate, db: Session = Depends(get_db)):
    """Atualiza dados de um fornecedor."""
    return service.atualizar_fornecedor(db, fornecedor_id, data)


@router.delete("/{fornecedor_id}")
def desativar(fornecedor_id: int, db: Session = Depends(get_db)):
    """Desativa (soft delete) um fornecedor."""
    return service.desativar_fornecedor(db, fornecedor_id)

@router.patch("/{fornecedor_id}/toggle-ativo")
def toggle_ativo(fornecedor_id: int, db: Session = Depends(get_db)):
    """Ativa ou desativa um fornecedor."""
    return service.toggle_ativo_fornecedor(db, fornecedor_id)

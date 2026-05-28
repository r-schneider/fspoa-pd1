from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.fornecedor_repository import FornecedorRepository
from app.schemas.schemas import FornecedorCreate, FornecedorUpdate, FornecedorResponse

repo = FornecedorRepository()


def criar_fornecedor(db: Session, data: FornecedorCreate) -> FornecedorResponse:
    existente = repo.find_by_cnpj(db, data.cnpj)
    if existente and existente.ativo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um fornecedor ativo com o CNPJ {data.cnpj}."
        )
    if existente and not existente.ativo:
        existente.ativo = True
        existente.nome = data.nome
        existente.email = data.email
        existente.telefone = data.telefone
        existente.endereco = data.endereco
        db.commit()
        db.refresh(existente)
        return FornecedorResponse.model_validate(existente)
    fornecedor = repo.create(db, data)
    return FornecedorResponse.model_validate(fornecedor)


def listar_fornecedores(db: Session) -> list[FornecedorResponse]:
    fornecedores = repo.find_all(db)
    return [FornecedorResponse.model_validate(f) for f in fornecedores]


def buscar_fornecedor(db: Session, fornecedor_id: int) -> FornecedorResponse:
    fornecedor = repo.find_by_id(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    return FornecedorResponse.model_validate(fornecedor)


def atualizar_fornecedor(db: Session, fornecedor_id: int, data: FornecedorUpdate) -> FornecedorResponse:
    fornecedor = repo.find_by_id(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    atualizado = repo.update(db, fornecedor, data)
    return FornecedorResponse.model_validate(atualizado)


def desativar_fornecedor(db: Session, fornecedor_id: int) -> dict:
    fornecedor = repo.find_by_id(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    repo.delete(db, fornecedor)
    return {"mensagem": "Fornecedor desativado com sucesso."}

def toggle_ativo_fornecedor(db: Session, fornecedor_id: int) -> dict:
    fornecedor = repo.find_by_id(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    fornecedor.ativo = not fornecedor.ativo
    db.commit()
    return {"id": fornecedor_id, "ativo": fornecedor.ativo}
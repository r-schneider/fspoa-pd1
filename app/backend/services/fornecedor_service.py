from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.backend.models.fornecedor_model import Fornecedor
from app.backend.repositories.fornecedor_repository import FornecedorRepository
from app.backend.schemas.fornecedor_schema import FornecedorCriar, FornecedorAtualizar


class FornecedorService:
    def __init__(self, db: Session):
        self.repo = FornecedorRepository(db)

    def criar(self, data: FornecedorCriar) -> Fornecedor:
        if data.cnpj and self.repo.cnpj_existe(data.cnpj):
            raise HTTPException(status_code=409, detail=f"CNPJ '{data.cnpj}' já cadastrado")
        fornecedor = Fornecedor(**data.model_dump())
        return self.repo.criar(fornecedor)

    def buscar_por_id(self, fornecedor_id: int) -> Fornecedor:
        fornecedor = self.repo.buscar_por_id(fornecedor_id)
        if not fornecedor:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
        return fornecedor

    def buscar_todos(self, somente_ativos: bool = False) -> List[Fornecedor]:
        if somente_ativos:
            return self.repo.buscar_todos_ativos()
        return self.repo.buscar_todos()

    def atualizar(self, fornecedor_id: int, data: FornecedorAtualizar) -> Fornecedor:
        fornecedor = self.buscar_por_id(fornecedor_id)
        if data.cnpj and self.repo.cnpj_existe(data.cnpj, excluir_id=fornecedor_id):
            raise HTTPException(status_code=409, detail=f"CNPJ '{data.cnpj}' já em uso")
        for chave, valor in data.model_dump(exclude_unset=True).items():
            setattr(fornecedor, chave, valor)
        return self.repo.atualizar(fornecedor)

    def deletar(self, fornecedor_id: int) -> None:
        fornecedor = self.buscar_por_id(fornecedor_id)
        if fornecedor.movimentacoes:
            raise HTTPException(
                status_code=409,
                detail="Fornecedor possui movimentações associadas. Desative-o em vez de excluir."
            )
        self.repo.deletar(fornecedor)

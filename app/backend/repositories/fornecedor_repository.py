from typing import Optional, List
from sqlalchemy.orm import Session

from app.backend.models.fornecedor_model import Fornecedor
from app.backend.repositories.base_repository import BaseRepository


class FornecedorRepository(BaseRepository[Fornecedor]):
    def __init__(self, db: Session):
        super().__init__(Fornecedor, db)

    def buscar_por_cnpj(self, cnpj: str) -> Optional[Fornecedor]:
        return self.db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

    def buscar_todos_ativos(self) -> List[Fornecedor]:
        return self.db.query(Fornecedor).filter(Fornecedor.ativo == True).all()

    def cnpj_existe(self, cnpj: str, excluir_id: int = None) -> bool:
        if not cnpj:
            return False
        query = self.db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj)
        if excluir_id:
            query = query.filter(Fornecedor.id != excluir_id)
        return query.first() is not None

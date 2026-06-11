from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.backend.models.categoria_model import Categoria
from app.backend.models.produto_model import Produto
from app.backend.repositories.base_repository import BaseRepository


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, db: Session):
        super().__init__(Categoria, db)

    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.nome == nome).first()

    def buscar_todos_ativos(self) -> List[Categoria]:
        return self.db.query(Categoria).filter(Categoria.ativo == True).all()

    def buscar_com_contagem_produtos(self):
        return (
            self.db.query(Categoria, func.count(Produto.id).label("contagem_produtos"))
            .outerjoin(Produto, (Produto.categoria_id == Categoria.id) & (Produto.ativo == True))
            .group_by(Categoria.id)
            .all()
        )

    def nome_existe(self, nome: str, excluir_id: int = None) -> bool:
        query = self.db.query(Categoria).filter(Categoria.nome == nome)
        if excluir_id:
            query = query.filter(Categoria.id != excluir_id)
        return query.first() is not None

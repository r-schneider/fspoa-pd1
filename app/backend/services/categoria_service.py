from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.backend.models.categoria_model import Categoria
from app.backend.repositories.categoria_repository import CategoriaRepository
from app.backend.schemas.categoria_schema import CategoriaCriar, CategoriaAtualizar, CategoriaComContagem


class CategoriaService:
    def __init__(self, db: Session):
        self.repo = CategoriaRepository(db)

    def criar(self, data: CategoriaCriar) -> Categoria:
        if self.repo.nome_existe(data.nome):
            raise HTTPException(status_code=409, detail="Categoria com este nome já existe")
        categoria = Categoria(nome=data.nome, descricao=data.descricao)
        return self.repo.criar(categoria)

    def buscar_por_id(self, categoria_id: int) -> Categoria:
        categoria = self.repo.buscar_por_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return categoria

    def buscar_todos(self, somente_ativos: bool = False) -> List[Categoria]:
        if somente_ativos:
            return self.repo.buscar_todos_ativos()
        return self.repo.buscar_todos()

    def buscar_todos_com_contagem(self) -> List[CategoriaComContagem]:
        rows = self.repo.buscar_com_contagem_produtos()
        result = []
        for categoria, contagem in rows:
            item = CategoriaComContagem.model_validate(categoria)
            item.contagem_produtos = contagem
            result.append(item)
        return result

    def atualizar(self, categoria_id: int, data: CategoriaAtualizar) -> Categoria:
        categoria = self.buscar_por_id(categoria_id)
        if data.nome and self.repo.nome_existe(data.nome, excluir_id=categoria_id):
            raise HTTPException(status_code=409, detail="Categoria com este nome já existe")
        if data.nome is not None:
            categoria.nome = data.nome
        if data.descricao is not None:
            categoria.descricao = data.descricao
        if data.ativo is not None:
            categoria.ativo = data.ativo
        return self.repo.atualizar(categoria)

    def deletar(self, categoria_id: int) -> None:
        categoria = self.buscar_por_id(categoria_id)
        if categoria.produtos:
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir categoria com produtos associados. Desative-a ou realoque os produtos."
            )
        self.repo.deletar(categoria)

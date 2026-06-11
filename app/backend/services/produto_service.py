from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.backend.models.produto_model import Produto
from app.backend.repositories.produto_repository import ProdutoRepository
from app.backend.repositories.categoria_repository import CategoriaRepository
from app.backend.schemas.produto_schema import ProdutoCriar, ProdutoAtualizar


class ProdutoService:
    def __init__(self, db: Session):
        self.repo = ProdutoRepository(db)
        self.repo_categoria = CategoriaRepository(db)

    def _gerar_sku(self, categoria_id: Optional[int]) -> str:
        prefixo = "PRO"
        if categoria_id:
            cat = self.repo_categoria.buscar_por_id(categoria_id)
            if cat:
                prefixo = cat.nome[:3].upper()
        numero = self.repo.proximo_numero_sku(prefixo)
        return f"{prefixo}-{numero:04d}"

    def criar(self, data: ProdutoCriar) -> Produto:
        if data.sku:
            if self.repo.sku_existe(data.sku):
                raise HTTPException(status_code=409, detail=f"SKU '{data.sku}' já cadastrado")
            sku = data.sku
        else:
            sku = self._gerar_sku(data.categoria_id)

        if data.codigo_barras and self.repo.codigo_barras_existe(data.codigo_barras):
            raise HTTPException(status_code=409, detail=f"Código de barras '{data.codigo_barras}' já cadastrado")
        if data.categoria_id:
            cat = self.repo_categoria.buscar_por_id(data.categoria_id)
            if not cat:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

        dados = data.model_dump()
        dados["sku"] = sku
        produto = Produto(**dados)
        return self.repo.criar(produto)

    def buscar_por_id(self, produto_id: int) -> Produto:
        produto = self.repo.buscar_por_id_com_categoria(produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto

    def pesquisar(
        self,
        busca: str = None,
        categoria_id: int = None,
        ativo: bool = None,
        estoque_baixo: bool = False,
        sem_estoque: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Produto]:
        return self.repo.pesquisar(busca, categoria_id, ativo, estoque_baixo, sem_estoque, skip, limit)

    def atualizar(self, produto_id: int, data: ProdutoAtualizar) -> Produto:
        produto = self.buscar_por_id(produto_id)

        if data.sku and self.repo.sku_existe(data.sku, excluir_id=produto_id):
            raise HTTPException(status_code=409, detail=f"SKU '{data.sku}' já em uso")
        if data.codigo_barras and self.repo.codigo_barras_existe(data.codigo_barras, excluir_id=produto_id):
            raise HTTPException(status_code=409, detail="Código de barras já em uso")
        if data.categoria_id:
            cat = self.repo_categoria.buscar_por_id(data.categoria_id)
            if not cat:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

        for chave, valor in data.model_dump(exclude_unset=True).items():
            setattr(produto, chave, valor)

        return self.repo.atualizar(produto)

    def deletar(self, produto_id: int) -> None:
        produto = self.buscar_por_id(produto_id)
        if produto.movimentacoes:
            raise HTTPException(
                status_code=409,
                detail="Produto possui movimentações. Desative-o em vez de excluir."
            )
        self.repo.deletar(produto)

    def alertas_estoque_baixo(self) -> List[Produto]:
        return self.repo.buscar_estoque_baixo()

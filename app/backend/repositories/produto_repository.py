from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func

from app.backend.models.produto_model import Produto
from app.backend.repositories.base_repository import BaseRepository


class ProdutoRepository(BaseRepository[Produto]):
    def __init__(self, db: Session):
        super().__init__(Produto, db)

    def buscar_por_id_com_categoria(self, produto_id: int) -> Optional[Produto]:
        return (
            self.db.query(Produto)
            .options(joinedload(Produto.categoria))
            .filter(Produto.id == produto_id)
            .first()
        )

    def buscar_por_sku(self, sku: str) -> Optional[Produto]:
        return self.db.query(Produto).filter(Produto.sku == sku).first()

    def buscar_por_codigo_barras(self, codigo_barras: str) -> Optional[Produto]:
        return self.db.query(Produto).filter(Produto.codigo_barras == codigo_barras).first()

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
        q = self.db.query(Produto).options(joinedload(Produto.categoria))

        if busca:
            q = q.filter(
                or_(
                    Produto.nome.ilike(f"%{busca}%"),
                    Produto.sku.ilike(f"%{busca}%"),
                    Produto.codigo_barras.ilike(f"%{busca}%"),
                )
            )
        if categoria_id is not None:
            q = q.filter(Produto.categoria_id == categoria_id)
        if ativo is not None:
            q = q.filter(Produto.ativo == ativo)
        if sem_estoque:
            q = q.filter(Produto.estoque_atual == 0)
        elif estoque_baixo:
            q = q.filter(Produto.estoque_atual <= Produto.estoque_minimo)

        return q.order_by(Produto.nome).offset(skip).limit(limit).all()

    def buscar_estoque_baixo(self) -> List[Produto]:
        return (
            self.db.query(Produto)
            .filter(Produto.ativo == True, Produto.estoque_atual <= Produto.estoque_minimo)
            .order_by(Produto.estoque_atual)
            .all()
        )

    def sku_existe(self, sku: str, excluir_id: int = None) -> bool:
        query = self.db.query(Produto).filter(Produto.sku == sku)
        if excluir_id:
            query = query.filter(Produto.id != excluir_id)
        return query.first() is not None

    def codigo_barras_existe(self, codigo_barras: str, excluir_id: int = None) -> bool:
        if not codigo_barras:
            return False
        query = self.db.query(Produto).filter(Produto.codigo_barras == codigo_barras)
        if excluir_id:
            query = query.filter(Produto.id != excluir_id)
        return query.first() is not None

    def contar_ativos(self) -> int:
        return self.db.query(Produto).filter(Produto.ativo == True).count()

    def contar_sem_estoque(self) -> int:
        return self.db.query(Produto).filter(Produto.ativo == True, Produto.estoque_atual == 0).count()

    def contar_estoque_baixo(self) -> int:
        return (
            self.db.query(Produto)
            .filter(Produto.ativo == True, Produto.estoque_atual <= Produto.estoque_minimo, Produto.estoque_atual > 0)
            .count()
        )

    def estoque_por_categoria(self) -> List:
        from app.backend.models.categoria_model import Categoria
        from sqlalchemy import case
        rows = (
            self.db.query(
                Categoria.nome.label("categoria"),
                func.count(Produto.id).label("total_produtos"),
                func.sum(
                    Produto.estoque_atual * func.coalesce(Produto.preco_custo, Produto.preco, 0)
                ).label("valor_total"),
            )
            .join(Produto, Produto.categoria_id == Categoria.id, isouter=True)
            .filter(Produto.ativo == True)
            .group_by(Categoria.id, Categoria.nome)
            .order_by(func.count(Produto.id).desc())
            .all()
        )
        return rows

    def proximo_numero_sku(self, prefixo: str) -> int:
        ultimo = (
            self.db.query(func.max(Produto.sku))
            .filter(Produto.sku.like(f"{prefixo}-%"))
            .scalar()
        )
        if ultimo:
            try:
                return int(ultimo.split("-")[1]) + 1
            except (IndexError, ValueError):
                pass
        return 1

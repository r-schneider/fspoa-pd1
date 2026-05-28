from sqlalchemy.orm import Session
from app.models.models import MovimentoEstoque, Produto
from app.schemas.schemas import MovimentoCreate


class MovimentoRepository:

    def create(self, db: Session, data: MovimentoCreate) -> MovimentoEstoque:
        movimento = MovimentoEstoque(**data.model_dump())
        db.add(movimento)

        # Atualiza estoque do produto
        produto = db.query(Produto).filter(Produto.id == data.produto_id).first()
        if produto:
            if data.tipo == "ENTRADA":
                produto.estoque_atual += data.quantidade
            elif data.tipo == "SAIDA":
                produto.estoque_atual -= data.quantidade

        db.commit()
        db.refresh(movimento)
        return movimento

    def find_all(self, db: Session, tipo: str | None = None) -> list[MovimentoEstoque]:
        query = db.query(MovimentoEstoque).order_by(MovimentoEstoque.criado_em.desc())
        if tipo:
            query = query.filter(MovimentoEstoque.tipo == tipo)
        return query.all()

    def find_by_produto(self, db: Session, produto_id: int) -> list[MovimentoEstoque]:
        return (
            db.query(MovimentoEstoque)
            .filter(MovimentoEstoque.produto_id == produto_id)
            .order_by(MovimentoEstoque.criado_em.desc())
            .all()
        )

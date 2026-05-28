from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.movimento_repository import MovimentoRepository
from app.models.models import Produto
from app.schemas.schemas import MovimentoCreate, MovimentoResponse

repo = MovimentoRepository()


def registrar_saida(db: Session, data: MovimentoCreate) -> MovimentoResponse:
    if data.tipo != "SAIDA":
        raise HTTPException(status_code=400, detail="Use este endpoint apenas para saídas.")

    produto = db.query(Produto).filter(Produto.id == data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if produto.estoque_atual < data.quantidade:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Estoque insuficiente. Disponível: {produto.estoque_atual} "
                f"{produto.unidade_medida.value}, solicitado: {data.quantidade}."
            )
        )

    movimento = repo.create(db, data)
    response = MovimentoResponse.model_validate(movimento)
    response.produto_nome = produto.nome
    return response


def listar_saidas(db: Session) -> list[MovimentoResponse]:
    movimentos = repo.find_all(db, tipo="SAIDA")
    result = []
    for m in movimentos:
        r = MovimentoResponse.model_validate(m)
        r.produto_nome = m.produto.nome if m.produto else None
        result.append(r)
    return result


def listar_todos_movimentos(db: Session) -> list[MovimentoResponse]:
    movimentos = repo.find_all(db)
    result = []
    for m in movimentos:
        r = MovimentoResponse.model_validate(m)
        r.produto_nome = m.produto.nome if m.produto else None
        result.append(r)
    return result

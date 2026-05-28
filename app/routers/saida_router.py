from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import MovimentoCreate, MovimentoResponse, ProdutoBasico
from app.models.models import Produto
import app.services.movimento_service as service

router = APIRouter(prefix="/saidas", tags=["Saída de Estoque"])


@router.post("/", response_model=MovimentoResponse, status_code=201)
def registrar_saida(data: MovimentoCreate, db: Session = Depends(get_db)):
    """
    Registra uma saída de estoque.
    O campo `tipo` deve ser **"SAIDA"**.
    Motivos aceitos: Venda, Uso interno, Produto danificado, Perda.
    """
    return service.registrar_saida(db, data)


@router.get("/", response_model=list[MovimentoResponse])
def listar_saidas(db: Session = Depends(get_db)):
    """Lista todas as saídas registradas."""
    return service.listar_saidas(db)


@router.get("/produtos", response_model=list[ProdutoBasico])
def listar_produtos_para_saida(db: Session = Depends(get_db)):
    """Retorna produtos com estoque > 0 para popular o dropdown de saída."""
    produtos = db.query(Produto).filter(
        Produto.ativo == True,
        Produto.estoque_atual > 0
    ).order_by(Produto.nome).all()
    return [ProdutoBasico.model_validate(p) for p in produtos]

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoriaCriar(BaseModel):
    nome: str
    descricao: Optional[str] = None


class CategoriaAtualizar(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None


class CategoriaResposta(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True


class CategoriaComContagem(CategoriaResposta):
    contagem_produtos: int = 0

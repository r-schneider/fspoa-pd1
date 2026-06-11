from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FornecedorCriar(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


class FornecedorAtualizar(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None


class FornecedorResposta(BaseModel):
    id: int
    nome: str
    cnpj: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True

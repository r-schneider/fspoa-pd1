from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ─── FORNECEDOR ───────────────────────────────────────────────

class FornecedorCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    cnpj: str = Field(..., min_length=14, max_length=18)
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    email: Optional[str]
    telefone: Optional[str]
    endereco: Optional[str]
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True


# ─── PRODUTO (simplificado para dropdowns) ────────────────────

class ProdutoBasico(BaseModel):
    id: int
    nome: str
    estoque_atual: int
    unidade_medida: str

    class Config:
        from_attributes = True


# ─── MOVIMENTO DE ESTOQUE ─────────────────────────────────────

class MovimentoCreate(BaseModel):
    produto_id: int
    tipo: str = Field(..., pattern="^(ENTRADA|SAIDA)$")
    motivo: str = Field(..., min_length=2, max_length=50)
    quantidade: int = Field(..., gt=0)
    responsavel: Optional[str] = None
    observacoes: Optional[str] = None


class MovimentoResponse(BaseModel):
    id: int
    tipo: str
    motivo: str
    quantidade: int
    responsavel: Optional[str]
    observacoes: Optional[str]
    criado_em: datetime
    produto_id: int
    produto_nome: Optional[str] = None

    class Config:
        from_attributes = True

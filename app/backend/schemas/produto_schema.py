from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

from app.backend.enums.estoque_enum import UnidadeMedida
from app.backend.schemas.categoria_schema import CategoriaResposta


class ProdutoCriar(BaseModel):
    nome: str
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    sku: Optional[str] = None
    estoque_minimo: int = 0
    estoque_maximo: Optional[int] = None
    preco: Decimal
    preco_custo: Optional[Decimal] = None
    unidade_medida: UnidadeMedida
    categoria_id: Optional[int] = None
    url_imagem: Optional[str] = None

    @field_validator("preco", "preco_custo", mode="before")
    @classmethod
    def preco_nao_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError("Preço não pode ser negativo")
        return v

    @field_validator("estoque_minimo")
    @classmethod
    def estoque_nao_negativo(cls, v):
        if v < 0:
            raise ValueError("Estoque mínimo não pode ser negativo")
        return v


class ProdutoAtualizar(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    sku: Optional[str] = None
    estoque_minimo: Optional[int] = None
    estoque_maximo: Optional[int] = None
    preco: Optional[Decimal] = None
    preco_custo: Optional[Decimal] = None
    unidade_medida: Optional[UnidadeMedida] = None
    categoria_id: Optional[int] = None
    ativo: Optional[bool] = None
    url_imagem: Optional[str] = None


class ProdutoResposta(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    codigo_barras: Optional[str]
    sku: str
    estoque_atual: int
    estoque_minimo: int
    estoque_maximo: Optional[int]
    preco: Decimal
    preco_custo: Optional[Decimal]
    unidade_medida: UnidadeMedida
    ativo: bool
    url_imagem: Optional[str]
    estoque_baixo: bool
    sem_estoque: bool
    categoria_id: Optional[int]
    categoria: Optional[CategoriaResposta]
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


class ProdutoListaResposta(BaseModel):
    id: int
    nome: str
    sku: str
    codigo_barras: Optional[str]
    estoque_atual: int
    estoque_minimo: int
    preco: Decimal
    unidade_medida: UnidadeMedida
    ativo: bool
    estoque_baixo: bool
    sem_estoque: bool
    categoria: Optional[CategoriaResposta]

    class Config:
        from_attributes = True

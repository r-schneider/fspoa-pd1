from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.backend.models.movimentacao_estoque_model import MovimentacaoEstoque
from app.backend.repositories.produto_repository import ProdutoRepository
from app.backend.repositories.movimentacao_estoque_repository import MovimentacaoEstoqueRepository
from app.backend.enums.estoque_enum import TipoMovimentacao, DirecaoMovimentacao
from app.backend.schemas.movimentacao_estoque_schema import EntradaEstoqueCriar, SaidaEstoqueCriar, MovimentacaoEstoqueDetalhe


class MovimentacaoEstoqueService:
    def __init__(self, db: Session):
        self.repo = MovimentacaoEstoqueRepository(db)
        self.repo_produto = ProdutoRepository(db)

    def registrar_entrada(self, data: EntradaEstoqueCriar) -> MovimentacaoEstoque:
        produto = self.repo_produto.buscar_por_id(data.produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        if not produto.ativo:
            raise HTTPException(status_code=400, detail="Produto inativo não pode receber movimentações")

        estoque_antes = produto.estoque_atual
        produto.estoque_atual += data.quantidade

        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            fornecedor_id=data.fornecedor_id,
            tipo_movimentacao=data.tipo_movimentacao,
            direcao=DirecaoMovimentacao.ENTRADA,
            quantidade=data.quantidade,
            custo_unitario=data.custo_unitario,
            estoque_antes=estoque_antes,
            estoque_depois=produto.estoque_atual,
            motivo=data.motivo,
            documento_referencia=data.documento_referencia,
        )

        if data.custo_unitario:
            produto.preco_custo = data.custo_unitario

        self.repo_produto.atualizar(produto)
        return self.repo.criar(movimentacao)

    def registrar_saida(self, data: SaidaEstoqueCriar) -> MovimentacaoEstoque:
        produto = self.repo_produto.buscar_por_id(data.produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        if not produto.ativo:
            raise HTTPException(status_code=400, detail="Produto inativo não pode receber movimentações")
        if produto.estoque_atual < data.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente. Disponível: {produto.estoque_atual}, Solicitado: {data.quantidade}"
            )

        estoque_antes = produto.estoque_atual
        produto.estoque_atual -= data.quantidade

        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            tipo_movimentacao=data.tipo_movimentacao,
            direcao=DirecaoMovimentacao.SAIDA,
            quantidade=data.quantidade,
            preco_unitario=data.preco_unitario,
            estoque_antes=estoque_antes,
            estoque_depois=produto.estoque_atual,
            motivo=data.motivo,
            documento_referencia=data.documento_referencia,
        )

        self.repo_produto.atualizar(produto)
        return self.repo.criar(movimentacao)

    def buscar_historico(
        self,
        produto_id: int = None,
        tipo_movimentacao: TipoMovimentacao = None,
        data_inicio: datetime = None,
        data_fim: datetime = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[MovimentacaoEstoqueDetalhe]:
        movimentacoes = self.repo.buscar_com_detalhes(skip, limit, produto_id, tipo_movimentacao, data_inicio, data_fim)
        result = []
        for m in movimentacoes:
            item = MovimentacaoEstoqueDetalhe.model_validate(m)
            item.nome_produto = m.produto.nome if m.produto else ""
            item.sku_produto = m.produto.sku if m.produto else ""
            item.nome_fornecedor = m.fornecedor.nome if m.fornecedor else None
            result.append(item)
        return result

    def buscar_historico_produto(self, produto_id: int, skip: int = 0, limit: int = 50) -> List[MovimentacaoEstoque]:
        produto = self.repo_produto.buscar_por_id(produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return self.repo.buscar_por_produto(produto_id, skip, limit)

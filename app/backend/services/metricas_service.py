from decimal import Decimal
from sqlalchemy.orm import Session

from app.backend.repositories.produto_repository import ProdutoRepository
from app.backend.repositories.movimentacao_estoque_repository import MovimentacaoEstoqueRepository
from app.backend.enums.estoque_enum import DirecaoMovimentacao
from app.backend.schemas.metricas_schema import (
    MetricasDashboard, AlertaEstoqueBaixo, ProdutoRanking, DashboardCompleto,
    MovimentoPorDia, EstoquePorCategoria,
)


class MetricasService:
    def __init__(self, db: Session):
        self.repo_produto = ProdutoRepository(db)
        self.repo_movimentacao = MovimentacaoEstoqueRepository(db)

    def metricas_dashboard(self) -> MetricasDashboard:
        total = self.repo_produto.contar()
        ativos = self.repo_produto.contar_ativos()
        sem_estoque = self.repo_produto.contar_sem_estoque()
        estoque_baixo = self.repo_produto.contar_estoque_baixo()

        movimentacoes_hoje = self.repo_movimentacao.contar_hoje()
        entradas_hoje = self.repo_movimentacao.contar_hoje_por_direcao(DirecaoMovimentacao.ENTRADA)
        saidas_hoje = self.repo_movimentacao.contar_hoje_por_direcao(DirecaoMovimentacao.SAIDA)

        produtos = self.repo_produto.buscar_todos(limit=99999)
        valor_inventario = sum(
            (p.estoque_atual * (p.preco_custo or p.preco))
            for p in produtos
            if p.ativo and p.estoque_atual > 0
        )

        return MetricasDashboard(
            total_produtos=total,
            produtos_ativos=ativos,
            sem_estoque=sem_estoque,
            estoque_baixo=estoque_baixo,
            movimentacoes_hoje=movimentacoes_hoje,
            entradas_hoje=entradas_hoje,
            saidas_hoje=saidas_hoje,
            valor_inventario=Decimal(str(round(valor_inventario, 2))),
        )

    def alertas_estoque_baixo(self):
        produtos = self.repo_produto.buscar_estoque_baixo()
        return [
            AlertaEstoqueBaixo(
                produto_id=p.id,
                nome_produto=p.nome,
                sku=p.sku,
                estoque_atual=p.estoque_atual,
                estoque_minimo=p.estoque_minimo,
                deficit=p.estoque_minimo - p.estoque_atual,
            )
            for p in produtos
        ]

    def mais_vendidos(self, limit: int = 5):
        rows = self.repo_movimentacao.mais_vendidos(limit)
        result = []
        for row in rows:
            produto = self.repo_produto.buscar_por_id(row.produto_id)
            if produto:
                result.append(ProdutoRanking(
                    produto_id=produto.id,
                    nome_produto=produto.nome,
                    sku=produto.sku,
                    quantidade_total=row.quantidade_total,
                    receita_total=Decimal(str(round(row.receita_total or 0, 2))),
                ))
        return result

    def mais_comprados(self, limit: int = 5):
        rows = self.repo_movimentacao.mais_comprados(limit)
        result = []
        for row in rows:
            produto = self.repo_produto.buscar_por_id(row.produto_id)
            if produto:
                result.append(ProdutoRanking(
                    produto_id=produto.id,
                    nome_produto=produto.nome,
                    sku=produto.sku,
                    quantidade_total=row.quantidade_total,
                    receita_total=None,
                ))
        return result

    def movimentos_por_dia(self, dias: int = 7) -> list[MovimentoPorDia]:
        from datetime import date, timedelta
        rows = self.repo_movimentacao.resumo_por_dia(dias)

        mapa: dict[str, dict] = {}
        for row in rows:
            chave = str(row.dia)
            if chave not in mapa:
                mapa[chave] = {"entradas": 0, "saidas": 0}
            from app.backend.enums.estoque_enum import DirecaoMovimentacao
            if row.direcao == DirecaoMovimentacao.ENTRADA:
                mapa[chave]["entradas"] = row.contagem
            else:
                mapa[chave]["saidas"] = row.contagem

        hoje = date.today()
        resultado = []
        for i in range(dias - 1, -1, -1):
            d = str(hoje - timedelta(days=i))
            vals = mapa.get(d, {"entradas": 0, "saidas": 0})
            resultado.append(MovimentoPorDia(data=d, entradas=vals["entradas"], saidas=vals["saidas"]))
        return resultado

    def estoque_por_categoria(self) -> list[EstoquePorCategoria]:
        rows = self.repo_produto.estoque_por_categoria()
        return [
            EstoquePorCategoria(
                categoria=row.categoria,
                total_produtos=row.total_produtos or 0,
                valor_total=float(row.valor_total or 0),
            )
            for row in rows
        ]

    def dashboard_completo(self) -> DashboardCompleto:
        metricas = self.metricas_dashboard()
        alertas = self.alertas_estoque_baixo()
        vendidos = self.mais_vendidos()
        comprados = self.mais_comprados()
        recentes = self.repo_movimentacao.buscar_com_detalhes(skip=0, limit=10)

        movimentacoes_recentes = [
            {
                "id": m.id,
                "nome_produto": m.produto.nome if m.produto else "",
                "tipo_movimentacao": m.tipo_movimentacao.value,
                "direcao": m.direcao.value,
                "quantidade": m.quantidade,
                "criado_em": m.criado_em.isoformat(),
            }
            for m in recentes
        ]

        return DashboardCompleto(
            metricas=metricas,
            alertas_estoque=alertas,
            mais_vendidos=vendidos,
            mais_comprados=comprados,
            movimentacoes_recentes=movimentacoes_recentes,
        )

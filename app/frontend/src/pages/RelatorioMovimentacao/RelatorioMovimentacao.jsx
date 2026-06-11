import { useState, useEffect, useCallback } from "react";
import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { estoqueAPI } from "../../service/api";
import "./RelatorioMovimentacao.css";

const TIPO_API_MAP = {
  Entrada: "ENTRADA_COMPRA",
  "Entrada (ajuste)": "ENTRADA_AJUSTE",
  "Entrada (devolução)": "ENTRADA_DEVOLUCAO",
  Saída: "SAIDA_VENDA",
  "Saída (baixa)": "SAIDA_BAIXA",
  "Saída (ajuste)": "SAIDA_AJUSTE",
};

const ITEMS_POR_PAGINA = 25;

function mapTipo(tipo_movimentacao) {
  if (!tipo_movimentacao) return "Ajuste";
  if (tipo_movimentacao.includes("AJUSTE")) return "Ajuste";
  if (tipo_movimentacao.startsWith("ENTRADA")) return "Entrada";
  if (tipo_movimentacao.startsWith("SAIDA")) return "Saída";
  return "Ajuste";
}

function RelatorioMovimentacao() {
  const [movimentacoes, setMovimentacoes] = useState([]);
  const [filtroDataInicio, setFiltroDataInicio] = useState("");
  const [filtroDataFim, setFiltroDataFim] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("");
  const [filtroProduto, setFiltroProduto] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [pagina, setPagina] = useState(1);

  const buscarMovimentacoes = useCallback(async () => {
    setCarregando(true);
    try {
      const params = {
        limit: 200,
        ...(filtroDataInicio && { data_inicio: filtroDataInicio }),
        ...(filtroDataFim && { data_fim: filtroDataFim + "T23:59:59" }),
        ...(filtroTipo && { tipo_movimentacao: TIPO_API_MAP[filtroTipo] || undefined }),
      };
      const lista = await estoqueAPI.historico(params);
      setMovimentacoes(lista);
    } catch {
      setMovimentacoes([]);
    } finally {
      setCarregando(false);
    }
  }, [filtroDataInicio, filtroDataFim, filtroTipo]);

  useEffect(() => {
    buscarMovimentacoes();
  }, [buscarMovimentacoes]);

  useEffect(() => {
    setPagina(1);
  }, [filtroDataInicio, filtroDataFim, filtroTipo, filtroProduto]);

  const movimentacoesFiltradas = filtroProduto
    ? movimentacoes.filter((m) =>
        (m.nome_produto || "").toLowerCase().includes(filtroProduto.toLowerCase())
      )
    : movimentacoes;

  const totalEntradas = movimentacoesFiltradas
    .filter((m) => m.direcao === "ENTRADA")
    .reduce((s, m) => s + m.quantidade, 0);
  const totalSaidas = movimentacoesFiltradas
    .filter((m) => m.direcao === "SAIDA")
    .reduce((s, m) => s + m.quantidade, 0);
  const saldo = totalEntradas - totalSaidas;

  const totalPaginas = Math.ceil(movimentacoesFiltradas.length / ITEMS_POR_PAGINA);
  const paginaItems = movimentacoesFiltradas.slice(
    (pagina - 1) * ITEMS_POR_PAGINA,
    pagina * ITEMS_POR_PAGINA
  );

  function exportarCSV() {
    const headers = ["Data", "Tipo", "Produto", "Quantidade", "Referência/Doc.", "Motivo"];
    const rows = movimentacoesFiltradas.map((item) => [
      new Date(item.criado_em).toLocaleString("pt-BR"),
      mapTipo(item.tipo_movimentacao),
      item.nome_produto || "",
      item.direcao === "ENTRADA" ? `+${item.quantidade}` : `-${item.quantidade}`,
      item.documento_referencia || "",
      item.motivo || "",
    ]);
    const csv = [headers, ...rows]
      .map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `movimentacoes_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="relatorio-movimentacao">
      <div className="relatorio-card">
        <div className="relatorio-header">
          <PageHeader
            title="Relatório de Movimentação"
            subtitle="Histórico de entradas, saídas e ajustes do estoque"
          />
          {movimentacoesFiltradas.length > 0 && (
            <button className="btn-exportar" onClick={exportarCSV}>
              Exportar CSV
            </button>
          )}
        </div>

        <div className="relatorio-filters">
          <div className="filter-group">
            <label>Data início</label>
            <input
              type="date"
              value={filtroDataInicio}
              onChange={(e) => setFiltroDataInicio(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>Data fim</label>
            <input
              type="date"
              value={filtroDataFim}
              onChange={(e) => setFiltroDataFim(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>Tipo</label>
            <select value={filtroTipo} onChange={(e) => setFiltroTipo(e.target.value)}>
              <option value="">Todos os tipos</option>
              {Object.keys(TIPO_API_MAP).map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
          <div className="filter-group">
            <label>Produto</label>
            <input
              type="text"
              placeholder="Buscar produto..."
              value={filtroProduto}
              onChange={(e) => setFiltroProduto(e.target.value)}
            />
          </div>
        </div>

        {carregando && (
          <p style={{ padding: "1rem", color: "#667085" }}>Carregando movimentações...</p>
        )}

        {!carregando && movimentacoesFiltradas.length > 0 && (
          <div className="relatorio-totais">
            <span>{movimentacoesFiltradas.length} registro(s)</span>
            <span className="totais-sep">|</span>
            <span>Entradas: <strong className="entrada-text">+{totalEntradas}</strong></span>
            <span>Saídas: <strong className="saida-text">-{totalSaidas}</strong></span>
            <span>Saldo: <strong className={saldo >= 0 ? "entrada-text" : "saida-text"}>{saldo >= 0 ? "+" : ""}{saldo}</strong></span>
          </div>
        )}

        {!carregando && movimentacoesFiltradas.length === 0 && (
          <div className="relatorio-totais">
            <span style={{ color: "#667085" }}>Nenhuma movimentação encontrada</span>
          </div>
        )}

        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Tipo</th>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Referência/Doc.</th>
              <th>Motivo</th>
            </tr>
          </thead>

          <tbody>
            {paginaItems.map((item) => {
              const tipo = mapTipo(item.tipo_movimentacao);
              const qtd =
                item.direcao === "ENTRADA"
                  ? `+${item.quantidade}`
                  : `-${item.quantidade}`;
              return (
                <tr key={item.id}>
                  <td>{new Date(item.criado_em).toLocaleString("pt-BR")}</td>
                  <td>
                    <StatusBadge status={tipo} />
                  </td>
                  <td>{item.nome_produto || "—"}</td>
                  <td
                    className={
                      item.direcao === "ENTRADA" ? "entrada-text" : "saida-text"
                    }
                  >
                    {qtd}
                  </td>
                  <td>{item.documento_referencia || "—"}</td>
                  <td>{item.motivo || "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {totalPaginas > 1 && (
          <div className="paginacao">
            <button
              className="paginacao-btn"
              disabled={pagina === 1}
              onClick={() => setPagina((p) => p - 1)}
            >
              ‹ Anterior
            </button>
            <span className="paginacao-info">
              Página {pagina} de {totalPaginas}
            </span>
            <button
              className="paginacao-btn"
              disabled={pagina === totalPaginas}
              onClick={() => setPagina((p) => p + 1)}
            >
              Próxima ›
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

export default RelatorioMovimentacao;

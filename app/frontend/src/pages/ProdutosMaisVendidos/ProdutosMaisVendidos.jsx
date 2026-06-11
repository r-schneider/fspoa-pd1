import { useState, useEffect } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from "recharts";
import PageHeader from "../../components/PageHeader/PageHeader";
import { dashboardAPI } from "../../service/api";
import "./ProdutosMaisVendidos.css";

function formatarReceita(valor) {
  const n = parseFloat(valor) || 0;
  if (n >= 1_000_000) return `R$ ${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `R$ ${(n / 1_000).toFixed(1)}K`;
  return `R$ ${n.toFixed(2).replace(".", ",")}`;
}

function truncar(str, max = 22) {
  return str.length > max ? str.slice(0, max - 1) + "…" : str;
}

function ProdutosMaisVendidos() {
  const [abaAtiva, setAbaAtiva] = useState("vendidos");
  const [vendas, setVendas] = useState([]);
  const [compras, setCompras] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    setCarregando(true);
    Promise.all([
      dashboardAPI.maisVendidos(10),
      dashboardAPI.maisComprados(10),
    ])
      .then(([v, c]) => {
        setVendas(v);
        setCompras(c);
      })
      .catch(() => {})
      .finally(() => setCarregando(false));
  }, []);

  const dados = abaAtiva === "vendidos" ? vendas : compras;

  const receitaTotal = abaAtiva === "vendidos"
    ? dados.reduce((s, d) => s + parseFloat(d.receita_total || 0), 0)
    : 0;
  const totalItens = dados.reduce((s, d) => s + (d.quantidade_total || 0), 0);
  const ticketMedio = totalItens > 0 ? receitaTotal / totalItens : 0;
  const maiorLote = dados.length > 0 ? Math.max(...dados.map((d) => d.quantidade_total || 0)) : 0;

  const kpis = abaAtiva === "vendidos"
    ? [
        { label: "Receita Total", valor: formatarReceita(receitaTotal) },
        { label: "Itens Saídos", valor: totalItens.toLocaleString("pt-BR") },
        { label: "Ticket Médio", valor: totalItens > 0 ? formatarReceita(ticketMedio) : "—" },
      ]
    : [
        { label: "Total Comprado", valor: `${totalItens.toLocaleString("pt-BR")} un` },
        { label: "Produtos no Ranking", valor: String(dados.length) },
        { label: "Maior Lote", valor: `${maiorLote.toLocaleString("pt-BR")} un` },
      ];

  const chartData = dados.slice(0, 8).map((item) => ({
    name: truncar(item.nome_produto),
    quantidade: item.quantidade_total,
  }));

  return (
    <section className="produtos-mais-vendidos">
      <div className="vendidos-card">
        <PageHeader
          title="Análise de Vendas e Compras"
          subtitle="Ranking dos produtos com maior movimentação no período"
          buttonText="Exportar relatório"
        />

        <div className="analise-tabs">
          <button
            className={abaAtiva === "vendidos" ? "active" : ""}
            onClick={() => setAbaAtiva("vendidos")}
          >
            Mais Vendidos
          </button>
          <button
            className={abaAtiva === "comprados" ? "active" : ""}
            onClick={() => setAbaAtiva("comprados")}
          >
            Mais Comprados
          </button>
        </div>

        <div className="analise-kpis">
          {kpis.map((k) => (
            <div className="kpi-card" key={k.label}>
              <span className="kpi-label">{k.label}</span>
              <span className="kpi-valor">{k.valor}</span>
            </div>
          ))}
        </div>

        {!carregando && chartData.length > 0 && (
          <div className="analise-chart">
            <p className="analise-chart-titulo">
              {abaAtiva === "vendidos" ? "Top produtos por quantidade vendida" : "Top produtos por quantidade comprada"}
            </p>
            <ResponsiveContainer width="100%" height={Math.max(160, chartData.length * 36)}>
              <BarChart
                layout="vertical"
                data={chartData}
                margin={{ top: 4, right: 24, left: 0, bottom: 4 }}
              >
                <XAxis
                  type="number"
                  tick={{ fontSize: 11, fill: "#667085" }}
                  axisLine={false}
                  tickLine={false}
                  allowDecimals={false}
                />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={155}
                  tick={{ fontSize: 12, fill: "#334155" }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  formatter={(v) => [`${v} un`]}
                  contentStyle={{ borderRadius: 10, border: "1px solid #e5e7eb", fontSize: 13 }}
                />
                <Bar dataKey="quantidade" fill="#0f3554" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {carregando && (
          <p style={{ padding: "1rem", color: "#667085" }}>Carregando dados...</p>
        )}

        <table>
          <thead>
            <tr>
              <th>Posição</th>
              <th>Produto</th>
              <th>SKU</th>
              <th>Quantidade</th>
              {abaAtiva === "vendidos" && <th>Receita</th>}
            </tr>
          </thead>
          <tbody>
            {dados.map((item, index) => (
              <tr key={item.produto_id}>
                <td>{index + 1}</td>
                <td>{item.nome_produto}</td>
                <td>{item.sku || "—"}</td>
                <td>{item.quantidade_total}</td>
                {abaAtiva === "vendidos" && <td>{formatarReceita(item.receita_total)}</td>}
              </tr>
            ))}
            {!carregando && dados.length === 0 && (
              <tr>
                <td
                  colSpan={abaAtiva === "vendidos" ? 5 : 4}
                  style={{ textAlign: "center", color: "#667085" }}
                >
                  Nenhum dado disponível
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default ProdutosMaisVendidos;

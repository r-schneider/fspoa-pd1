import { useState, useEffect } from "react";
import {
  FaBox,
  FaTriangleExclamation,
  FaDollarSign,
  FaCartShopping,
  FaArrowTrendUp,
  FaArrowDown,
  FaArrowUp,
} from "react-icons/fa6";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

import CardMetric from "../../components/CardMetric/CardMetric";
import ProductTable from "../../components/ProductTable/ProductTable";
import { dashboardAPI, produtosAPI } from "../../service/api";

import "./Dashboard.css";

const CHART_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#0f3554", "#06b6d4"];

const DIAS_MAP = { Mês: 30, Semana: 7, Dia: 1 };

function formatarValor(valor) {
  const n = parseFloat(valor) || 0;
  if (n >= 1_000_000) return `R$ ${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `R$ ${(n / 1_000).toFixed(1)}K`;
  return `R$ ${n.toFixed(0)}`;
}

function formatarData(dataStr) {
  const [, mes, dia] = dataStr.split("-");
  return `${dia}/${mes}`;
}

function tempoRelativo(isoStr) {
  const diff = Math.floor((Date.now() - new Date(isoStr)) / 60000);
  if (diff < 1) return "agora";
  if (diff < 60) return `${diff}min`;
  const h = Math.floor(diff / 60);
  if (h < 24) return `${h}h`;
  return `${Math.floor(h / 24)}d`;
}

function Dashboard() {
  const [metricas, setMetricas] = useState(null);
  const [produtos, setProdutos] = useState([]);
  const [recentes, setRecentes] = useState([]);
  const [movimentos, setMovimentos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [periodoAtivo, setPeriodoAtivo] = useState("Semana");

  useEffect(() => {
    dashboardAPI.metricas().then(setMetricas).catch(() => {});
    produtosAPI.listar({ estoque_baixo: true, limit: 3 })
      .then((lista) => {
        if (lista.length === 0) return produtosAPI.listar({ limit: 3 });
        return lista;
      })
      .then(setProdutos)
      .catch(() => {});
    dashboardAPI.completo()
      .then((d) => setRecentes(d.movimentacoes_recentes || []))
      .catch(() => {});
    dashboardAPI.estoquePorCategoria().then(setCategorias).catch(() => {});
  }, []);

  useEffect(() => {
    dashboardAPI.movimentosPorDia(DIAS_MAP[periodoAtivo])
      .then(setMovimentos)
      .catch(() => {});
  }, [periodoAtivo]);

  return (
    <section className="dashboard">
      <div className="dashboard-cards">
        <CardMetric
          title="Total de Produtos"
          value={metricas ? String(metricas.total_produtos) : "—"}
          description={metricas ? `${metricas.sem_estoque} sem estoque` : "Carregando..."}
          icon={<FaBox />}
          color="blue"
        />
        <CardMetric
          title="Estoque Baixo"
          value={metricas ? String(metricas.estoque_baixo) : "—"}
          description={metricas ? `${metricas.sem_estoque} em nível crítico` : "Carregando..."}
          icon={<FaTriangleExclamation />}
          color="red"
          danger
        />
        <CardMetric
          title="Valor em Estoque"
          value={metricas ? formatarValor(metricas.valor_inventario) : "—"}
          description="Valor total do inventário"
          icon={<FaDollarSign />}
          color="green"
        />
        <CardMetric
          title="Movimentações Hoje"
          value={metricas ? String(metricas.movimentacoes_hoje) : "—"}
          description={
            metricas
              ? `↑ ${metricas.entradas_hoje} entradas  ↓ ${metricas.saidas_hoje} saídas`
              : "Carregando..."
          }
          icon={<FaCartShopping />}
          color="orange"
        />
        <CardMetric
          title="Saldo de Hoje"
          value={metricas ? (metricas.entradas_hoje - metricas.saidas_hoje >= 0 ? `+${metricas.entradas_hoje - metricas.saidas_hoje}` : String(metricas.entradas_hoje - metricas.saidas_hoje)) : "—"}
          description={metricas ? `↑ ${metricas.entradas_hoje} entradas  ↓ ${metricas.saidas_hoje} saídas` : "Carregando..."}
          icon={<FaArrowTrendUp />}
          color={metricas && metricas.entradas_hoje - metricas.saidas_hoje < 0 ? "red" : "green"}
        />
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card chart-card">
          <div className="section-title">
            <div>
              <h3>Movimentações de Estoque</h3>
              <p>Entradas e saídas no período</p>
            </div>
            <div className="chart-tabs">
              {Object.keys(DIAS_MAP).map((p) => (
                <button
                  key={p}
                  className={periodoAtivo === p ? "active" : ""}
                  onClick={() => setPeriodoAtivo(p)}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={movimentos} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
              <XAxis
                dataKey="data"
                tickFormatter={formatarData}
                tick={{ fontSize: 11, fill: "#667085" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                allowDecimals={false}
                tick={{ fontSize: 11, fill: "#667085" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                formatter={(v, name) => [v, name === "entradas" ? "Entradas" : "Saídas"]}
                labelFormatter={(l) => formatarData(l)}
                contentStyle={{ borderRadius: 10, border: "1px solid #e5e7eb", fontSize: 13 }}
              />
              <Bar dataKey="entradas" fill="#10b981" radius={[4, 4, 0, 0]} name="Entradas" />
              <Bar dataKey="saidas" fill="#ef4444" radius={[4, 4, 0, 0]} name="Saídas" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="dashboard-card category-card">
          <h3>Distribuição por Categoria</h3>

          {categorias.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={categorias}
                  dataKey="total_produtos"
                  nameKey="categoria"
                  innerRadius={55}
                  outerRadius={88}
                  paddingAngle={3}
                >
                  {categorias.map((_, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(v, name) => [`${v} produtos`, name]}
                  contentStyle={{ borderRadius: 10, border: "1px solid #e5e7eb", fontSize: 13 }}
                />
                <Legend
                  iconType="circle"
                  iconSize={8}
                  formatter={(v) => <span style={{ fontSize: 12, color: "#667085" }}>{v}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="donut-empty">Sem categorias cadastradas</div>
          )}
        </div>
      </div>

      {recentes.length > 0 && (
        <div className="dashboard-card recentes-card">
          <h3>Movimentações Recentes</h3>
          <ul className="recentes-list">
            {recentes.slice(0, 6).map((m) => (
              <li key={m.id} className="recente-item">
                <span className={`recente-icon ${m.direcao === "ENTRADA" ? "entrada" : "saida"}`}>
                  {m.direcao === "ENTRADA" ? <FaArrowDown /> : <FaArrowUp />}
                </span>
                <span className="recente-nome">{m.nome_produto}</span>
                <span className={`recente-qtd ${m.direcao === "ENTRADA" ? "entrada-text" : "saida-text"}`}>
                  {m.direcao === "ENTRADA" ? "+" : "-"}{m.quantidade}
                </span>
                <span className="recente-tempo">{tempoRelativo(m.criado_em)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <ProductTable
        produtos={produtos}
        onDelete={async (produto) => {
          if (!window.confirm(`Remover "${produto.nome}"?`)) return;
          try {
            await produtosAPI.deletar(produto.id);
            setProdutos((prev) => prev.filter((p) => p.id !== produto.id));
          } catch (err) {
            alert(err.message);
          }
        }}
      />
    </section>
  );
}

export default Dashboard;

import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { FaBox, FaArrowDown, FaTriangleExclamation } from "react-icons/fa6";
import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { produtosAPI, categoriasAPI } from "../../service/api";
import "./VisualizarEstoque.css";

function getStatus(produto) {
  if (produto.sem_estoque) return "Crítico";
  if (produto.estoque_baixo) return "Atenção";
  return "Estável";
}

function getScoreCriticidade(p) {
  if (p.sem_estoque) return 2;
  if (p.estoque_baixo) return 1;
  return 0;
}

function getBarClass(status) {
  if (status === "Crítico") return "bar-red";
  if (status === "Atenção") return "bar-yellow";
  return "bar-green";
}

function getBarWidth(stock, minStock) {
  if (!minStock || minStock === 0) return "100%";
  return `${Math.min((stock / minStock) * 100, 100)}%`;
}

function VisualizarEstoque() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [produtos, setProdutos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [busca, setBusca] = useState(searchParams.get("q") || "");
  const [filtroStatus, setFiltroStatus] = useState("Todos");
  const [filtroCategoria, setFiltroCategoria] = useState("");

  useEffect(() => {
    setCarregando(true);
    Promise.all([
      produtosAPI.listar({ limit: 200 }),
      categoriasAPI.listar(),
    ])
      .then(([prods, cats]) => {
        setProdutos(prods);
        setCategorias(cats);
      })
      .catch(() => {})
      .finally(() => setCarregando(false));
  }, []);

  const produtosFiltrados = produtos.filter((p) => {
    if (busca && !p.nome.toLowerCase().includes(busca.toLowerCase()) &&
        !(p.sku || "").toLowerCase().includes(busca.toLowerCase())) return false;
    if (filtroStatus !== "Todos" && getStatus(p) !== filtroStatus) return false;
    if (filtroCategoria && String(p.categoria_id) !== filtroCategoria) return false;
    return true;
  });

  const produtosCriticos = [...produtos]
    .sort((a, b) => getScoreCriticidade(b) - getScoreCriticidade(a))
    .slice(0, 3);

  return (
    <section className="visualizar-estoque">
      <div className="stock-summary">
        {produtosCriticos.map((produto) => {
          const status = getStatus(produto);
          return (
            <div className="stock-card" key={produto.id}>
              <div className={`stock-icon ${status === "Crítico" ? "stock-icon-critico" : status === "Atenção" ? "stock-icon-atencao" : ""}`}>
                {status !== "Estável" ? <FaTriangleExclamation /> : <FaBox />}
              </div>
              <div>
                <h4>{produto.nome}</h4>
                <p>
                  {produto.estoque_atual}{" "}
                  {produto.unidade_medida?.toLowerCase() || "un"}
                  {" · "}
                  <StatusBadge status={status} />
                </p>
                {produto.estoque_minimo > 0 && produto.estoque_atual < produto.estoque_minimo && (
                  <span className="deficit-info">
                    Déficit: {produto.estoque_minimo - produto.estoque_atual} {produto.unidade_medida?.toLowerCase() || "un"}
                  </span>
                )}
              </div>
              <div className="bar-wrapper">
                <span className="bar-legenda">
                  {produto.estoque_atual} de {produto.estoque_minimo} mínimo
                </span>
                <div className="bar">
                  <span
                    className={getBarClass(status)}
                    style={{ width: getBarWidth(produto.estoque_atual, produto.estoque_minimo) }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="stock-table-card">
        <PageHeader
          title="Visualizar Dados do Estoque"
          subtitle="Acompanhamento geral dos produtos cadastrados"
          buttonText="Registrar entrada"
          onButtonClick={() => navigate("/entrada")}
        />

        <div className="stock-filters">
          <input
            type="text"
            placeholder="Buscar por nome ou SKU..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
          <select value={filtroStatus} onChange={(e) => setFiltroStatus(e.target.value)}>
            <option value="Todos">Todos os status</option>
            <option value="Crítico">Crítico</option>
            <option value="Atenção">Atenção</option>
            <option value="Estável">Estável</option>
          </select>
          <select value={filtroCategoria} onChange={(e) => setFiltroCategoria(e.target.value)}>
            <option value="">Todas as categorias</option>
            {categorias.map((c) => (
              <option key={c.id} value={String(c.id)}>{c.nome}</option>
            ))}
          </select>
        </div>

        {carregando && (
          <p style={{ padding: "1rem", color: "#667085" }}>Carregando produtos...</p>
        )}

        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Categoria</th>
              <th>Estoque atual</th>
              <th>Mínimo</th>
              <th>SKU</th>
              <th>Status</th>
              <th>Ação</th>
            </tr>
          </thead>
          <tbody>
            {produtosFiltrados.map((produto) => (
              <tr key={produto.id}>
                <td>{produto.nome}</td>
                <td>{produto.categoria?.nome || "—"}</td>
                <td>
                  {produto.estoque_atual}{" "}
                  {produto.unidade_medida?.toLowerCase() || "un"}
                </td>
                <td>
                  {produto.estoque_minimo}{" "}
                  {produto.unidade_medida?.toLowerCase() || "un"}
                </td>
                <td>{produto.sku || "—"}</td>
                <td>
                  <StatusBadge status={getStatus(produto)} />
                </td>
                <td>
                  <button
                    className="btn-entrada-rapida"
                    title="Registrar entrada"
                    onClick={() => navigate(`/entrada?produto_id=${produto.id}`)}
                  >
                    <FaArrowDown />
                  </button>
                </td>
              </tr>
            ))}
            {!carregando && produtosFiltrados.length === 0 && (
              <tr>
                <td colSpan="7" style={{ textAlign: "center", color: "#667085" }}>
                  Nenhum produto encontrado
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default VisualizarEstoque;

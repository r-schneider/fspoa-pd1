import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { dashboardAPI, produtosAPI } from "../../service/api";
import "./AlertaEstoqueBaixo.css";

function AlertaEstoqueBaixo() {
  const navigate = useNavigate();
  const [alertas, setAlertas] = useState([]);
  const [proximosDoMinimo, setProximosDoMinimo] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardAPI.alertas(),
      produtosAPI.listar({ ativo: true, limit: 200 }),
    ])
      .then(([alertasData, todosProdutos]) => {
        setAlertas(alertasData);
        const alertaIds = new Set(alertasData.map((a) => a.produto_id));
        const proximos = todosProdutos.filter(
          (p) =>
            p.estoque_minimo > 0 &&
            !alertaIds.has(p.id) &&
            p.estoque_atual >= p.estoque_minimo &&
            p.estoque_atual <= p.estoque_minimo * 1.2
        );
        setProximosDoMinimo(proximos);
      })
      .catch(() => {})
      .finally(() => setCarregando(false));
  }, []);

  return (
    <section className="alerta-estoque-baixo">
      <div className="alerta-card">
        <PageHeader
          title="Alerta de Estoque Baixo"
          subtitle="Produtos abaixo do estoque mínimo"
          buttonText="Registrar entrada"
          onButtonClick={() => navigate("/entrada")}
        />

        <div className="alerta-info">
          <strong>{alertas.length} produtos precisam de atenção</strong>
          <span>
            Verifique os itens críticos e faça reposição quando necessário.
          </span>
        </div>

        {carregando && (
          <p style={{ padding: "1rem", color: "#667085" }}>Carregando alertas...</p>
        )}

        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Estoque atual</th>
              <th>Estoque mínimo</th>
              <th>Déficit</th>
              <th>Status</th>
              <th>Ação</th>
            </tr>
          </thead>

          <tbody>
            {alertas.map((item) => {
              const status =
                item.estoque_atual === 0 ||
                (item.estoque_minimo > 0 && item.estoque_atual / item.estoque_minimo < 0.5)
                  ? "Crítico"
                  : "Atenção";
              return (
                <tr key={item.produto_id}>
                  <td>{item.nome_produto}</td>
                  <td
                    className={
                      status === "Crítico" ? "estoque-critico" : "estoque-atencao"
                    }
                  >
                    {item.estoque_atual}
                  </td>
                  <td>{item.estoque_minimo}</td>
                  <td>{item.deficit}</td>
                  <td>
                    <StatusBadge status={status} />
                  </td>
                  <td>
                    <button
                      className="btn-repor"
                      onClick={() => navigate(`/entrada?produto_id=${item.produto_id}`)}
                    >
                      Repor
                    </button>
                  </td>
                </tr>
              );
            })}
            {!carregando && alertas.length === 0 && (
              <tr>
                <td
                  colSpan="6"
                  style={{ textAlign: "center", color: "#667085" }}
                >
                  Nenhum produto com estoque baixo
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {proximosDoMinimo.length > 0 && (
        <div className="alerta-card">
          <div className="proximos-header">
            <div>
              <h3 className="proximos-titulo">Próximos do Mínimo</h3>
              <p className="proximos-subtitulo">
                Produtos dentro de 20% do estoque mínimo — atenção preventiva
              </p>
            </div>
            <span className="proximos-badge">{proximosDoMinimo.length}</span>
          </div>

          <table>
            <thead>
              <tr>
                <th>Produto</th>
                <th>Estoque atual</th>
                <th>Estoque mínimo</th>
                <th>Folga</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              {proximosDoMinimo.map((p) => {
                const folga = p.estoque_atual - p.estoque_minimo;
                const percentFolga = Math.round((folga / p.estoque_minimo) * 100);
                return (
                  <tr key={p.id}>
                    <td>{p.nome}</td>
                    <td className="estoque-atencao">
                      {p.estoque_atual} {p.unidade_medida?.toLowerCase() || "un"}
                    </td>
                    <td>
                      {p.estoque_minimo} {p.unidade_medida?.toLowerCase() || "un"}
                    </td>
                    <td>+{folga} ({percentFolga}%)</td>
                    <td>
                      <button
                        className="btn-repor"
                        onClick={() => navigate(`/entrada?produto_id=${p.id}`)}
                      >
                        Repor
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default AlertaEstoqueBaixo;

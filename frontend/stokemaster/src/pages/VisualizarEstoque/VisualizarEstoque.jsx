import { FaBox } from "react-icons/fa6";
import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { produtos } from "../../data/produtos";
import "./VisualizarEstoque.css";

function VisualizarEstoque() {
  const produtosResumo = produtos.slice(0, 3);

  function getBarClass(status) {
    if (status === "Crítico") return "bar-red";
    if (status === "Atenção") return "bar-yellow";
    return "bar-green";
  }

  function getBarWidth(stock, minStock) {
    const percentage = Math.min((stock / minStock) * 100, 100);
    return `${percentage}%`;
  }

  return (
    <section className="visualizar-estoque">
      <div className="stock-summary">
        {produtosResumo.map((produto) => (
          <div className="stock-card" key={produto.code}>
            <div className="stock-icon">
              <FaBox />
            </div>

            <div>
              <h4>{produto.name}</h4>
              <p>{produto.stock} unidades</p>
            </div>

            <div className="bar">
              <span
                className={getBarClass(produto.status)}
                style={{
                  width: getBarWidth(produto.stock, produto.minStock),
                }}
              ></span>
            </div>
          </div>
        ))}
      </div>

      <div className="stock-table-card">
        <PageHeader
          title="Visualizar Dados do Estoque"
          subtitle="Acompanhamento geral dos produtos cadastrados"
          buttonText="Atualizar estoque"
        />

        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Estoque atual</th>
              <th>Mínimo</th>
              <th>Local</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {produtos.map((produto) => (
              <tr key={produto.code}>
                <td>{produto.name}</td>
                <td>{produto.stock} unidades</td>
                <td>{produto.minStock} unidades</td>
                <td>{produto.location}</td>
                <td>
                  <StatusBadge status={produto.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default VisualizarEstoque;

import { useNavigate } from "react-router-dom";
import { FaBox, FaEye, FaPen, FaTrash } from "react-icons/fa6";
import StatusBadge from "../StatusBadge/StatusBadge";
import "./ProductTable.css";

function getStatus(produto) {
  if (produto.sem_estoque) return "Crítico";
  if (produto.estoque_baixo) return "Atenção";
  return "Estável";
}

function formatarPreco(preco) {
  return `R$ ${parseFloat(preco || 0)
    .toFixed(2)
    .replace(".", ",")}`;
}

function ProductTable({ produtos = [], onDelete }) {
  const navigate = useNavigate();

  return (
    <div className="product-table-card">
      <div className="table-header">
        <div>
          <h3>Atenção Necessária</h3>
          <p>Produtos com estoque baixo ou crítico</p>
        </div>
        <div>
          <button className="btn-light" onClick={() => navigate("/estoque")}>Ver todos</button>
          <button className="btn-light" onClick={() => navigate("/produtos")}>Gerenciar</button>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Produto</th>
            <th>Código</th>
            <th>Categoria</th>
            <th>Estoque</th>
            <th>Valor</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>

        <tbody>
          {produtos.map((produto) => (
            <tr key={produto.id}>
              <td>
                <div className="product-cell">
                  <div className="product-icon">
                    <FaBox />
                  </div>
                  {produto.nome}
                </div>
              </td>
              <td>{produto.sku || "—"}</td>
              <td>{produto.categoria?.nome || "—"}</td>
              <td>
                {produto.estoque_atual}{" "}
                {produto.unidade_medida?.toLowerCase() || "un"}
              </td>
              <td>{formatarPreco(produto.preco)}</td>
              <td>
                <StatusBadge status={getStatus(produto)} />
              </td>
              <td className="actions">
                <FaEye
                  title="Ver no estoque"
                  onClick={() => navigate(`/estoque?q=${encodeURIComponent(produto.nome)}`)}
                />
                <FaPen
                  title="Editar produto"
                  onClick={() => navigate("/produtos")}
                />
                <FaTrash
                  title="Remover produto"
                  style={{ color: "#ef4444" }}
                  onClick={() => onDelete && onDelete(produto)}
                />
              </td>
            </tr>
          ))}
          {produtos.length === 0 && (
            <tr>
              <td colSpan="7" style={{ textAlign: "center", color: "#667085" }}>
                Nenhum produto com atenção necessária
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ProductTable;

import { FaBox, FaEye, FaPen, FaTrash } from "react-icons/fa6";
import { produtos } from "../../data/produtos";
import StatusBadge from "../StatusBadge/StatusBadge";
import "./ProductTable.css";

function ProductTable() {
  return (
    <div className="product-table-card">
      <div className="table-header">
        <div>
          <h3>Status do Estoque</h3>
          <p>Produtos principais do inventário</p>
        </div>

        <div>
          <button className="btn-light">Filtrar</button>
          <button className="btn-light">Exportar</button>
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
            <tr key={produto.code}>
              <td>
                <div className="product-cell">
                  <div className="product-icon">
                    <FaBox />
                  </div>
                  {produto.name}
                </div>
              </td>

              <td>{produto.code}</td>
              <td>{produto.category}</td>
              <td>{produto.stock} unidades</td>
              <td>{produto.value}</td>

              <td>
                <StatusBadge status={produto.status} />
              </td>

              <td className="actions">
                <FaEye />
                <FaPen />
                <FaTrash />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductTable;

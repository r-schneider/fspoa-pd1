import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { movimentacoes } from "../../data/movimentacoes";
import "./RelatorioMovimentacao.css";

function RelatorioMovimentacao() {
  return (
    <section className="relatorio-movimentacao">
      <div className="relatorio-card">
        <PageHeader
          title="Relatório de Movimentação"
          subtitle="Histórico de entradas, saídas e ajustes do estoque"
          buttonText="Exportar PDF"
        />

        <div className="relatorio-filters">
          <input type="date" />
          <select>
            <option>Todos os tipos</option>
            <option>Entrada</option>
            <option>Saída</option>
            <option>Ajuste</option>
          </select>
          <input type="text" placeholder="Buscar produto" />
        </div>

        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Tipo</th>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Responsável</th>
              <th>Motivo</th>
            </tr>
          </thead>

          <tbody>
            {movimentacoes.map((item, index) => (
              <tr key={index}>
                <td>{item.data}</td>
                <td>
                  <StatusBadge status={item.tipo} />
                </td>
                <td>{item.produto}</td>
                <td
                  className={
                    item.quantidade.includes("-") ? "saida-text" : "entrada-text"
                  }
                >
                  {item.quantidade}
                </td>
                <td>{item.responsavel}</td>
                <td>{item.motivo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RelatorioMovimentacao;

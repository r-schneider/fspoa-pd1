import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { alertas } from "../../data/alertas";
import "./AlertaEstoqueBaixo.css";

function AlertaEstoqueBaixo() {
  return (
    <section className="alerta-estoque-baixo">
      <div className="alerta-card">
        <PageHeader
          title="Alerta de Estoque Baixo"
          subtitle="Produtos abaixo do estoque mínimo"
          buttonText="Solicitar compra"
        />

        <div className="alerta-info">
          <strong>{alertas.length} produtos precisam de atenção</strong>
          <span>
            Verifique os itens críticos e faça reposição quando necessário.
          </span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Estoque atual</th>
              <th>Estoque mínimo</th>
              <th>Previsão</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {alertas.map((item) => (
              <tr key={item.produto}>
                <td>{item.produto}</td>
                <td
                  className={
                    item.status === "Crítico"
                      ? "estoque-critico"
                      : "estoque-atencao"
                  }
                >
                  {item.estoqueAtual}
                </td>
                <td>{item.estoqueMinimo}</td>
                <td>{item.previsao}</td>
                <td>
                  <StatusBadge status={item.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default AlertaEstoqueBaixo;

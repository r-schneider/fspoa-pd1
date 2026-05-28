import {
  FaBox,
  FaTriangleExclamation,
  FaDollarSign,
  FaCartShopping,
} from "react-icons/fa6";

import CardMetric from "../../components/CardMetric/CardMetric";
import ProductTable from "../../components/ProductTable/ProductTable";
import "./Dashboard.css";

function Dashboard() {
  return (
    <section className="dashboard">
      <div className="dashboard-cards">
        <CardMetric
          title="Total de Produtos"
          value="1.248"
          description="↑ 12,5% este mês"
          icon={<FaBox />}
          color="blue"
        />

        <CardMetric
          title="Estoque Baixo"
          value="47"
          description="↑ 5 alertas hoje"
          icon={<FaTriangleExclamation />}
          color="red"
          danger
        />

        <CardMetric
          title="Valor em Estoque"
          value="R$ 284K"
          description="↑ 8,5% este mês"
          icon={<FaDollarSign />}
          color="green"
        />

        <CardMetric
          title="Vendas do Mês"
          value="R$ 97K"
          description="↑ 18% vs mês anterior"
          icon={<FaCartShopping />}
          color="orange"
        />
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card chart-card">
          <div className="section-title">
            <div>
              <h3>Controle de Estoque</h3>
              <p>Estoque atual x estoque ideal</p>
            </div>

            <div className="chart-tabs">
              <button className="active">Mês</button>
              <button>Semana</button>
              <button>Dia</button>
            </div>
          </div>

          <div className="chart">
            <div className="chart-line blue-line"></div>
            <div className="chart-line green-line"></div>

            <div className="chart-labels">
              <span>Jan</span>
              <span>Fev</span>
              <span>Mar</span>
              <span>Abr</span>
              <span>Mai</span>
              <span>Jun</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card category-card">
          <h3>Categorias</h3>

          <div className="donut-wrapper">
            <div className="donut"></div>

            <div className="legend">
              <span>
                <i className="dot blue-dot"></i> Eletrônicos
              </span>
              <span>
                <i className="dot green-dot"></i> Periféricos
              </span>
              <span>
                <i className="dot orange-dot"></i> Acessórios
              </span>
              <span>
                <i className="dot purple-dot"></i> Outros
              </span>
            </div>
          </div>
        </div>
      </div>

      <ProductTable />
    </section>
  );
}

export default Dashboard;

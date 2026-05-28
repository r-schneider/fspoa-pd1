import PageHeader from "../../components/PageHeader/PageHeader";
import { vendas } from "../../data/vendas";
import "./ProdutosMaisVendidos.css";

function ProdutosMaisVendidos() {
  const top3 = vendas.slice(0, 3);

  return (
    <section className="produtos-mais-vendidos">
      <div className="vendidos-card">
        <PageHeader
          title="Análise de Produtos Mais Vendidos"
          subtitle="Ranking dos produtos com maior saída no período"
          buttonText="Exportar relatório"
        />

        <div className="ranking-cards">
          {top3.map((item, index) => (
            <div
              className={index === 0 ? "ranking-card first" : "ranking-card"}
              key={item.posicao}
            >
              <span>Top {index + 1}</span>
              <h3>{item.produto}</h3>
              <p>{item.vendas} vendas</p>
            </div>
          ))}
        </div>

        <table>
          <thead>
            <tr>
              <th>Posição</th>
              <th>Produto</th>
              <th>Categoria</th>
              <th>Vendas</th>
              <th>Receita</th>
            </tr>
          </thead>

          <tbody>
            {vendas.map((item) => (
              <tr key={item.posicao}>
                <td>{item.posicao}</td>
                <td>{item.produto}</td>
                <td>{item.categoria}</td>
                <td>{item.vendas}</td>
                <td>{item.receita}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default ProdutosMaisVendidos;

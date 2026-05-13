import PageHeader from "../../components/PageHeader/PageHeader";
import "./SaidaEstoque.css";

function SaidaEstoque() {
  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Registrar Saída de Estoque"
          subtitle="Registre vendas, perdas ou retiradas internas"
        />

        <div className="movement-buttons saida-buttons">
          <button className="movement-type active" type="button">
            Saída
          </button>
          <button className="movement-type" type="button">
            Venda
          </button>
          <button className="movement-type" type="button">
            Perda
          </button>
        </div>

        <form className="form-grid">
          <input type="text" placeholder="Produto" />
          <input type="number" placeholder="Quantidade" />

          <select>
            <option>Venda</option>
            <option>Uso interno</option>
            <option>Produto danificado</option>
          </select>

          <input type="text" placeholder="Responsável" />

          <textarea placeholder="Observações"></textarea>

          <button className="btn-submit" type="submit">
            Registrar saída
          </button>
        </form>
      </div>
    </section>
  );
}

export default SaidaEstoque;

import PageHeader from "../../components/PageHeader/PageHeader";
import "./EntradaEstoque.css";

function EntradaEstoque() {
  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Registrar Entrada de Estoque"
          subtitle="Adicione quantidades aos produtos existentes"
        />

        <div className="movement-buttons entrada-buttons">
          <button className="movement-type active" type="button">
            Entrada
          </button>
          <button className="movement-type" type="button">
            Ajuste
          </button>
        </div>

        <form className="form-grid">
          <input type="text" placeholder="Produto" />
          <input type="number" placeholder="Quantidade" />

          <select>
            <option>Compra</option>
            <option>Devolução</option>
            <option>Ajuste manual</option>
          </select>

          <input type="datetime-local" />

          <textarea placeholder="Observações"></textarea>

          <button className="btn-submit" type="submit">
            Registrar entrada
          </button>
        </form>
      </div>
    </section>
  );
}

export default EntradaEstoque;

import PageHeader from "../../components/PageHeader/PageHeader";
import "./CadastroProduto.css";

function CadastroProduto() {
  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Cadastro de Produtos"
          subtitle="Adicione novos produtos ao estoque"
        />

        <form className="form-grid">
          <input type="text" placeholder="Nome do produto" />
          <input type="text" placeholder="Código/SKU" />
          <input type="text" placeholder="Categoria" />
          <input type="text" placeholder="Fornecedor" />
          <input type="number" placeholder="Preço unitário" />
          <input type="number" placeholder="Estoque mínimo" />

          <textarea placeholder="Descrição do produto"></textarea>

          <button className="btn-submit" type="submit">
            Salvar produto
          </button>
        </form>
      </div>
    </section>
  );
}

export default CadastroProduto;

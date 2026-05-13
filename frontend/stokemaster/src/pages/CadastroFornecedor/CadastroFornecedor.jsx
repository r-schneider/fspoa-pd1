import PageHeader from "../../components/PageHeader/PageHeader";
import "./CadastroFornecedor.css";

function CadastroFornecedor() {
  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Cadastro de Fornecedor"
          subtitle="Registre empresas responsáveis pelo fornecimento dos produtos"
        />

        <form className="form-grid">
          <input type="text" placeholder="Nome da empresa" />
          <input type="text" placeholder="CNPJ" />
          <input type="email" placeholder="E-mail" />
          <input type="text" placeholder="Telefone" />
          <input className="full-input" type="text" placeholder="Endereço" />

          <button className="btn-submit" type="submit">
            Salvar fornecedor
          </button>
        </form>
      </div>
    </section>
  );
}

export default CadastroFornecedor;

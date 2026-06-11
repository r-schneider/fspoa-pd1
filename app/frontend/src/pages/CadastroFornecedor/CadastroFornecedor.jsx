import { useState, useEffect } from "react";
import { FaTrash } from "react-icons/fa6";
import PageHeader from "../../components/PageHeader/PageHeader";
import { fornecedoresAPI } from "../../service/api";
import "./CadastroFornecedor.css";

const FORM_INICIAL = {
  nome: "",
  cnpj: "",
  email: "",
  telefone: "",
  endereco: "",
};

function formatarCNPJ(valor) {
  return valor
    .replace(/\D/g, "")
    .replace(/^(\d{2})(\d)/, "$1.$2")
    .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    .replace(/\.(\d{3})(\d)/, ".$1/$2")
    .replace(/(\d{4})(\d)/, "$1-$2")
    .slice(0, 18);
}

function formatarTelefone(valor) {
  return valor
    .replace(/\D/g, "")
    .replace(/^(\d{2})(\d)/, "($1) $2")
    .replace(/(\d{5})(\d{4})$/, "$1-$2")
    .slice(0, 15);
}

function CadastroFornecedor() {
  const [form, setForm] = useState(FORM_INICIAL);
  const [fornecedores, setFornecedores] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [busca, setBusca] = useState("");
  const [editando, setEditando] = useState(null);

  useEffect(() => {
    carregarFornecedores();
  }, []);

  async function carregarFornecedores() {
    try {
      const lista = await fornecedoresAPI.listar();
      setFornecedores(lista);
    } catch {
      // silencioso
    }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    let v = value;
    if (name === "cnpj") v = formatarCNPJ(value);
    if (name === "telefone") v = formatarTelefone(value);
    setForm((f) => ({ ...f, [name]: v }));
    setErro("");
    setSucesso("");
  }

  function handleCancelar() {
    setEditando(null);
    setForm(FORM_INICIAL);
    setErro("");
    setSucesso("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    setSucesso("");

    if (!form.nome.trim() || !form.cnpj.trim()) {
      setErro("Nome e CNPJ são obrigatórios.");
      return;
    }

    setCarregando(true);
    try {
      if (editando) {
        await fornecedoresAPI.atualizar(editando.id, form);
        setSucesso(`Fornecedor "${form.nome}" atualizado com sucesso!`);
        setEditando(null);
      } else {
        await fornecedoresAPI.cadastrar(form);
        setSucesso(`Fornecedor "${form.nome}" cadastrado com sucesso!`);
      }
      setForm(FORM_INICIAL);
      carregarFornecedores();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  async function handleToggle(id, ativoAtual) {
    try {
      await fornecedoresAPI.alternarAtivo(id, ativoAtual);
      carregarFornecedores();
    } catch {
      setErro("Erro ao alterar status do fornecedor.");
    }
  }

  async function handleDeletar(fornecedor) {
    if (!window.confirm(`Deletar fornecedor "${fornecedor.nome}"? Esta ação não pode ser desfeita.`)) return;
    try {
      await fornecedoresAPI.desativar(fornecedor.id);
      setSucesso(`Fornecedor "${fornecedor.nome}" removido.`);
      if (editando?.id === fornecedor.id) handleCancelar();
      carregarFornecedores();
    } catch (err) {
      setErro(err.message || "Erro ao deletar fornecedor.");
    }
  }

  async function handleEditar(fornecedor) {
    setEditando(fornecedor);
    setForm({
      nome: fornecedor.nome,
      cnpj: fornecedor.cnpj,
      email: fornecedor.email || "",
      telefone: fornecedor.telefone || "",
      endereco: fornecedor.endereco || "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const listaFiltrada = fornecedores.filter((f) =>
    !busca || f.nome.toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title={editando ? `Editando: ${editando.nome}` : "Cadastro de Fornecedor"}
          subtitle="Registre empresas responsáveis pelo fornecimento dos produtos"
        />

        {erro && <div className="alert alert-erro">{erro}</div>}
        {sucesso && <div className="alert alert-sucesso">{sucesso}</div>}

        <form className="form-grid" onSubmit={handleSubmit}>
          <input
            type="text"
            name="nome"
            placeholder="Nome da empresa *"
            value={form.nome}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="cnpj"
            placeholder="CNPJ *"
            value={form.cnpj}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="E-mail"
            value={form.email}
            onChange={handleChange}
          />
          <input
            type="text"
            name="telefone"
            placeholder="Telefone"
            value={form.telefone}
            onChange={handleChange}
          />
          <input
            className="full-input"
            type="text"
            name="endereco"
            placeholder="Endereço"
            value={form.endereco}
            onChange={handleChange}
          />

          <div className="form-actions">
            <button className="btn-submit" type="submit" disabled={carregando}>
              {carregando ? "Salvando..." : editando ? "Atualizar fornecedor" : "Salvar fornecedor"}
            </button>
            {editando && (
              <button type="button" className="btn-cancelar" onClick={handleCancelar}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      {fornecedores.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <div className="forn-list-header">
            <h3>Fornecedores cadastrados ({fornecedores.length})</h3>
            <input
              className="forn-busca"
              type="text"
              placeholder="Buscar fornecedor..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          <table className="fornecedor-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>CNPJ</th>
                <th>E-mail</th>
                <th>Telefone</th>
                <th>Ativo</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {listaFiltrada.map((f) => (
                <tr key={f.id}>
                  <td>{f.nome}</td>
                  <td>{f.cnpj}</td>
                  <td>{f.email || "—"}</td>
                  <td>{f.telefone || "—"}</td>
                  <td>
                    <label className="switch">
                      <input
                        type="checkbox"
                        checked={f.ativo}
                        onChange={() => handleToggle(f.id, f.ativo)}
                      />
                      <span className="slider"></span>
                    </label>
                  </td>
                  <td className="table-acoes">
                    <button className="btn-editar" onClick={() => handleEditar(f)}>
                      Editar
                    </button>
                    <button
                      className="btn-deletar btn-icon"
                      onClick={() => handleDeletar(f)}
                      title={`Remover ${f.nome}`}
                    >
                      <FaTrash />
                    </button>
                  </td>
                </tr>
              ))}
              {listaFiltrada.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: "center", color: "#667085" }}>
                    Nenhum fornecedor encontrado
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default CadastroFornecedor;

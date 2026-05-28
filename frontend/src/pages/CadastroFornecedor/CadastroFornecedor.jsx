import { useState, useEffect } from "react";
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
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [filtro, setFiltro] = useState("ativos");
  const [editando, setEditando] = useState(null);

  useEffect(() => {
    carregarFornecedores();
  }, []);

  async function carregarFornecedores() {
    try {
      const lista = await fornecedoresAPI.listar();
      setFornecedores(lista);
    } catch {
      // silencioso — lista é secundária
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

  async function handleToggle(id) {
    try {
      await fetch(`http://localhost:8000/fornecedores/${id}/toggle-ativo`, { method: "PATCH" });
      carregarFornecedores();
    } catch {
      setErro("Erro ao alterar status do fornecedor.");
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

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Cadastro de Fornecedor"
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

          <button className="btn-submit" type="submit" disabled={carregando}>
            {carregando ? "Salvando..." : editando ? "Atualizar fornecedor" : "Salvar fornecedor"}
          </button>
        </form>
      </div>

      {/* Lista de fornecedores cadastrados */}
      {fornecedores.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <h3>Fornecedores cadastrados</h3>
            <div style={{ display: "flex", gap: "6px" }}>
              {["ativos", "inativos", "todos"].map((f) => (
                <button
                  key={f}
                  onClick={() => setFiltro(f)}
                  style={{
                    padding: "5px 14px",
                    borderRadius: "6px",
                    border: "0.5px solid #e2e8f0",
                    background: filtro === f ? "#f1f5f9" : "transparent",
                    fontWeight: filtro === f ? "500" : "400",
                    cursor: "pointer",
                    fontSize: "12px",
                    textTransform: "capitalize",
                  }}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          <table className="fornecedor-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>CNPJ</th>
                <th>E-mail</th>
                <th>Telefone</th>
                <th>Status</th>
                <th>Ativo</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {fornecedores
                .filter((f) =>
                  filtro === "ativos" ? f.ativo :
                  filtro === "inativos" ? !f.ativo : true
                )
                .map((f) => (
                  <tr key={f.id}>
                    <td>{f.nome}</td>
                    <td>{f.cnpj}</td>
                    <td>{f.email || "—"}</td>
                    <td>{f.telefone || "—"}</td>
                    <td>
                      <span style={{
                        fontSize: "11px", fontWeight: "500", padding: "2px 8px",
                        borderRadius: "20px",
                        background: f.ativo ? "#dcfce7" : "#f1f5f9",
                        color: f.ativo ? "#15803d" : "#64748b",
                      }}>
                        {f.ativo ? "Ativo" : "Inativo"}
                      </span>
                    </td>
                    <td>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={f.ativo}
                          onChange={() => handleToggle(f.id)}
                        />
                        <span className="slider"></span>
                      </label>
                    </td>
                    <td>
                      <button
                        className="btn-editar"
                        onClick={() => handleEditar(f)}
                      >
                        Editar
                      </button>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default CadastroFornecedor;

import { useState, useEffect } from "react";
import { FaTrash } from "react-icons/fa6";
import PageHeader from "../../components/PageHeader/PageHeader";
import { categoriasAPI } from "../../service/api";
import "./Categorias.css";

const FORM_INICIAL = { nome: "", descricao: "" };

function Categorias() {
  const [form, setForm] = useState(FORM_INICIAL);
  const [categorias, setCategorias] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [editando, setEditando] = useState(null);
  const [busca, setBusca] = useState("");

  useEffect(() => {
    carregarCategorias();
  }, []);

  async function carregarCategorias() {
    try {
      const lista = await categoriasAPI.listar();
      setCategorias(lista);
    } catch { /* silencioso */ }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    setErro("");
    setSucesso("");
  }

  function handleEditar(cat) {
    setEditando(cat);
    setForm({ nome: cat.nome, descricao: cat.descricao || "" });
    window.scrollTo({ top: 0, behavior: "smooth" });
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

    if (!form.nome.trim()) {
      setErro("O nome da categoria é obrigatório.");
      return;
    }

    const payload = {
      nome: form.nome.trim(),
      ...(form.descricao.trim() && { descricao: form.descricao.trim() }),
    };

    setCarregando(true);
    try {
      if (editando) {
        await categoriasAPI.atualizar(editando.id, payload);
        setSucesso(`Categoria "${form.nome}" atualizada com sucesso!`);
        setEditando(null);
      } else {
        await categoriasAPI.criar(payload);
        setSucesso(`Categoria "${form.nome}" criada com sucesso!`);
      }
      setForm(FORM_INICIAL);
      carregarCategorias();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  async function handleToggle(id, ativoAtual) {
    try {
      await categoriasAPI.atualizar(id, { ativo: !ativoAtual });
      carregarCategorias();
    } catch {
      setErro("Erro ao alterar status da categoria.");
    }
  }

  async function handleDeletar(cat) {
    if (!window.confirm(`Deletar a categoria "${cat.nome}"?`)) return;
    try {
      await categoriasAPI.deletar(cat.id);
      setSucesso(`Categoria "${cat.nome}" removida.`);
      carregarCategorias();
    } catch (err) {
      setErro(err.message);
    }
  }

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title={editando ? `Editando: ${editando.nome}` : "Gestão de Categorias"}
          subtitle={
            editando
              ? "Atualize os dados da categoria"
              : "Organize seus produtos em categorias"
          }
        />

        {erro && <div className="alert alert-erro">{erro}</div>}
        {sucesso && <div className="alert alert-sucesso">{sucesso}</div>}

        <form className="form-grid" onSubmit={handleSubmit}>
          <input
            type="text"
            name="nome"
            placeholder="Nome da categoria *"
            value={form.nome}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="descricao"
            placeholder="Descrição (opcional)"
            value={form.descricao}
            onChange={handleChange}
          />
          <div className="form-actions">
            <button className="btn-submit" type="submit" disabled={carregando}>
              {carregando ? "Salvando..." : editando ? "Atualizar categoria" : "Criar categoria"}
            </button>
            {editando && (
              <button type="button" className="btn-cancelar" onClick={handleCancelar}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      {categorias.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <div className="cat-list-header">
            <h3>Categorias cadastradas ({categorias.length})</h3>
            <input
              className="cat-busca"
              type="text"
              placeholder="Buscar categoria..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          {(() => {
            const lista = [...categorias]
              .filter((c) => !busca || c.nome.toLowerCase().includes(busca.toLowerCase()))
              .sort((a, b) => {
                const diff = (b.contagem_produtos ?? 0) - (a.contagem_produtos ?? 0);
                return diff !== 0 ? diff : a.nome.localeCompare(b.nome, "pt-BR");
              });
            return (
              <table className="categorias-table">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Produtos</th>
                    <th>Ativo</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {lista.map((cat) => (
                    <tr key={cat.id}>
                      <td>{cat.nome}</td>
                      <td>{cat.descricao || "—"}</td>
                      <td>
                        <span className="badge-count">{cat.contagem_produtos ?? 0}</span>
                      </td>
                      <td>
                        <label className="switch">
                          <input
                            type="checkbox"
                            checked={cat.ativo}
                            onChange={() => handleToggle(cat.id, cat.ativo)}
                          />
                          <span className="slider" />
                        </label>
                      </td>
                      <td className="table-acoes">
                        <button className="btn-editar" onClick={() => handleEditar(cat)}>
                          Editar
                        </button>
                        <button
                          className="btn-deletar btn-icon"
                          onClick={() => handleDeletar(cat)}
                          disabled={(cat.contagem_produtos ?? 0) > 0}
                          title={
                            (cat.contagem_produtos ?? 0) > 0
                              ? "Remova os produtos vinculados antes de deletar"
                              : "Deletar categoria"
                          }
                        >
                          <FaTrash />
                        </button>
                      </td>
                    </tr>
                  ))}
                  {lista.length === 0 && (
                    <tr>
                      <td colSpan="5" style={{ textAlign: "center", color: "#667085" }}>
                        Nenhuma categoria encontrada
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            );
          })()}
        </div>
      )}
    </section>
  );
}

export default Categorias;

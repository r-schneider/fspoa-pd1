import { useState, useEffect } from "react";
import { FaTrash } from "react-icons/fa6";
import PageHeader from "../../components/PageHeader/PageHeader";
import StatusBadge from "../../components/StatusBadge/StatusBadge";
import { produtosAPI, categoriasAPI } from "../../service/api";
import "./CadastroProduto.css";

const UNIDADES = [
  { value: "UNIDADE", label: "Unidade" },
  { value: "METRO", label: "Metro" },
  { value: "LITRO", label: "Litro" },
  { value: "QUILOGRAMA", label: "Quilograma" },
  { value: "CAIXA", label: "Caixa" },
  { value: "PACOTE", label: "Pacote" },
  { value: "ROLO", label: "Rolo" },
  { value: "PAR", label: "Par" },
];

const FORM_INICIAL = {
  nome: "",
  codigo_barras: "",
  sku: "",
  categoria_id: "",
  unidade_medida: "UNIDADE",
  preco: "",
  preco_custo: "",
  estoque_minimo: "0",
  estoque_maximo: "",
  descricao: "",
};

function getStatus(produto) {
  if (produto.sem_estoque) return "Crítico";
  if (produto.estoque_baixo) return "Atenção";
  return "Estável";
}

function CadastroProduto() {
  const [form, setForm] = useState(FORM_INICIAL);
  const [categorias, setCategorias] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [editando, setEditando] = useState(null);

  useEffect(() => {
    categoriasAPI.listar().then(setCategorias).catch(() => {});
    carregarProdutos();
  }, []);

  async function carregarProdutos() {
    try {
      const lista = await produtosAPI.listar({ limit: 100 });
      setProdutos(lista);
    } catch { /* silencioso */ }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    setErro("");
    setSucesso("");
  }

  function handleEditar(produto) {
    setEditando(produto);
    setForm({
      nome: produto.nome || "",
      codigo_barras: produto.codigo_barras || "",
      sku: produto.sku || "",
      categoria_id: produto.categoria_id ? String(produto.categoria_id) : "",
      unidade_medida: produto.unidade_medida || "UNIDADE",
      preco: produto.preco != null ? String(produto.preco) : "",
      preco_custo: produto.preco_custo != null ? String(produto.preco_custo) : "",
      estoque_minimo: produto.estoque_minimo != null ? String(produto.estoque_minimo) : "0",
      estoque_maximo: produto.estoque_maximo != null ? String(produto.estoque_maximo) : "",
      descricao: produto.descricao || "",
    });
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
      setErro("O nome do produto é obrigatório.");
      return;
    }
    if (!form.preco || Number(form.preco) < 0) {
      setErro("Informe um preço válido.");
      return;
    }

    const payload = {
      nome: form.nome.trim(),
      preco: Number(form.preco),
      unidade_medida: form.unidade_medida,
      estoque_minimo: Number(form.estoque_minimo) || 0,
      ...(form.codigo_barras.trim() && { codigo_barras: form.codigo_barras.trim() }),
      ...(form.sku.trim() && { sku: form.sku.trim() }),
      ...(form.categoria_id && { categoria_id: Number(form.categoria_id) }),
      ...(form.preco_custo && { preco_custo: Number(form.preco_custo) }),
      ...(form.estoque_maximo && { estoque_maximo: Number(form.estoque_maximo) }),
      ...(form.descricao.trim() && { descricao: form.descricao.trim() }),
    };

    setCarregando(true);
    try {
      if (editando) {
        await produtosAPI.atualizar(editando.id, payload);
        setSucesso(`Produto "${form.nome}" atualizado com sucesso!`);
        setEditando(null);
      } else {
        await produtosAPI.criar(payload);
        setSucesso(`Produto "${form.nome}" cadastrado com sucesso!`);
      }
      setForm(FORM_INICIAL);
      carregarProdutos();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  async function handleDeletar(produto) {
    if (!window.confirm(`Deletar "${produto.nome}"? Esta ação não pode ser desfeita.`)) return;
    try {
      await produtosAPI.deletar(produto.id);
      setSucesso(`Produto "${produto.nome}" removido.`);
      carregarProdutos();
    } catch (err) {
      setErro(err.message);
    }
  }

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title={editando ? `Editando: ${editando.nome}` : "Cadastro de Produtos"}
          subtitle={editando ? "Atualize os dados do produto" : "Adicione novos produtos ao estoque"}
        />

        {erro && <div className="alert alert-erro">{erro}</div>}
        {sucesso && <div className="alert alert-sucesso">{sucesso}</div>}

        <form className="form-grid" onSubmit={handleSubmit}>
          <input
            type="text"
            name="nome"
            placeholder="Nome do produto *"
            value={form.nome}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="codigo_barras"
            placeholder="Código de barras"
            value={form.codigo_barras}
            onChange={handleChange}
          />
          <select name="categoria_id" value={form.categoria_id} onChange={handleChange}>
            <option value="">Categoria (opcional)</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>{c.nome}</option>
            ))}
          </select>
          <select name="unidade_medida" value={form.unidade_medida} onChange={handleChange} required>
            {UNIDADES.map((u) => (
              <option key={u.value} value={u.value}>{u.label}</option>
            ))}
          </select>
          <input
            type="number"
            name="preco"
            placeholder="Preço de venda *"
            value={form.preco}
            onChange={handleChange}
            min="0"
            step="0.01"
            required
          />
          <input
            type="number"
            name="preco_custo"
            placeholder="Preço de custo"
            value={form.preco_custo}
            onChange={handleChange}
            min="0"
            step="0.01"
          />
          <input
            type="number"
            name="estoque_minimo"
            placeholder="Estoque mínimo"
            value={form.estoque_minimo}
            onChange={handleChange}
            min="0"
          />
          <input
            type="number"
            name="estoque_maximo"
            placeholder="Estoque máximo"
            value={form.estoque_maximo}
            onChange={handleChange}
            min="0"
          />
          <input
            type="text"
            name="sku"
            placeholder="SKU (gerado automaticamente se vazio)"
            title="SKU: código interno do sistema. Código de barras: número impresso na embalagem do produto (EAN/GTIN)."
            value={form.sku}
            onChange={handleChange}
          />
          <textarea
            name="descricao"
            placeholder="Descrição do produto"
            value={form.descricao}
            onChange={handleChange}
          />
          <div className="form-actions">
            <button className="btn-submit" type="submit" disabled={carregando}>
              {carregando ? "Salvando..." : editando ? "Atualizar produto" : "Salvar produto"}
            </button>
            {editando && (
              <button type="button" className="btn-cancelar" onClick={handleCancelar}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      {produtos.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <h3 style={{ marginBottom: "1rem", color: "#111827" }}>
            Produtos cadastrados ({produtos.length})
          </h3>
          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>SKU</th>
                  <th>Categoria</th>
                  <th>Preço venda</th>
                  <th>Estoque</th>
                  <th>Status</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {produtos.map((p) => (
                  <tr key={p.id}>
                    <td>{p.nome}</td>
                    <td>{p.sku || "—"}</td>
                    <td>{p.categoria?.nome || "—"}</td>
                    <td>R$ {parseFloat(p.preco || 0).toFixed(2).replace(".", ",")}</td>
                    <td>{p.estoque_atual} {p.unidade_medida?.toLowerCase() || "un"}</td>
                    <td><StatusBadge status={getStatus(p)} /></td>
                    <td className="table-acoes">
                      <button className="btn-editar" onClick={() => handleEditar(p)}>Editar</button>
                      <button
                        className="btn-deletar btn-icon"
                        onClick={() => handleDeletar(p)}
                        title={`Remover ${p.nome}`}
                      >
                        <FaTrash />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </section>
  );
}

export default CadastroProduto;

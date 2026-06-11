import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import PageHeader from "../../components/PageHeader/PageHeader";
import { produtosAPI, estoqueAPI, fornecedoresAPI } from "../../service/api";
import "./EntradaEstoque.css";

const TIPOS_ENTRADA = {
  Compra: "ENTRADA_COMPRA",
  "Devolução": "ENTRADA_DEVOLUCAO",
};

const TIPOS_AJUSTE = {
  "Ajuste manual": "ENTRADA_AJUSTE",
};

const FORM_INICIAL = {
  produto_id: "",
  quantidade: "",
  sub_tipo: "Compra",
  custo_unitario: "",
  fornecedor_id: "",
  observacoes: "",
};

function EntradaEstoque() {
  const [searchParams] = useSearchParams();
  const [tipoAtivo, setTipoAtivo] = useState("Entrada");
  const [form, setForm] = useState(FORM_INICIAL);
  const [produtos, setProdutos] = useState([]);
  const [fornecedores, setFornecedores] = useState([]);
  const [historico, setHistorico] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");

  useEffect(() => {
    const pid = searchParams.get("produto_id");
    produtosAPI.listar({ ativo: true }).then((lista) => {
      setProdutos(lista);
      if (pid) setForm((f) => ({ ...f, produto_id: pid }));
    }).catch(() => {});
    fornecedoresAPI.listar({ somente_ativos: true }).then(setFornecedores).catch(() => {});
    carregarHistorico();
  }, []);

  async function carregarHistorico() {
    try {
      const lista = await estoqueAPI.historico({ limit: 20 });
      setHistorico(lista.filter((m) => m.direcao === "ENTRADA").slice(0, 10));
    } catch { /* silencioso */ }
  }

  function selecionarTipo(tipo) {
    setTipoAtivo(tipo);
    setForm((f) => ({
      ...f,
      sub_tipo: tipo === "Ajuste" ? "Ajuste manual" : "Compra",
      fornecedor_id: "",
    }));
    setErro("");
    setSucesso("");
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    setErro("");
    setSucesso("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    setSucesso("");

    if (!form.produto_id) {
      setErro("Selecione um produto.");
      return;
    }
    if (!form.quantidade || Number(form.quantidade) <= 0) {
      setErro("Informe uma quantidade válida.");
      return;
    }

    const tiposMap = tipoAtivo === "Ajuste" ? TIPOS_AJUSTE : TIPOS_ENTRADA;
    const tipo_movimentacao = tiposMap[form.sub_tipo];

    const payload = {
      produto_id: Number(form.produto_id),
      tipo_movimentacao,
      quantidade: Number(form.quantidade),
      ...(form.custo_unitario && { custo_unitario: Number(form.custo_unitario) }),
      ...(form.fornecedor_id && { fornecedor_id: Number(form.fornecedor_id) }),
      ...(form.observacoes.trim() && { motivo: form.observacoes.trim() }),
    };

    setCarregando(true);
    try {
      await estoqueAPI.registrarEntrada(payload);
      const nomeProduto =
        produtos.find((p) => p.id === Number(form.produto_id))?.nome ||
        `Produto #${form.produto_id}`;
      setSucesso(
        `Entrada de ${form.quantidade} unidade(s) de "${nomeProduto}" registrada!`
      );
      setForm({
        ...FORM_INICIAL,
        sub_tipo: tipoAtivo === "Ajuste" ? "Ajuste manual" : "Compra",
      });
      produtosAPI.listar({ ativo: true }).then(setProdutos).catch(() => {});
      carregarHistorico();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  const opcoesSubTipo =
    tipoAtivo === "Ajuste" ? Object.keys(TIPOS_AJUSTE) : Object.keys(TIPOS_ENTRADA);
  const mostrarFornecedor = tipoAtivo === "Entrada" && form.sub_tipo === "Compra";
  const produtoSelecionado = produtos.find((p) => p.id === Number(form.produto_id));
  const estoqueApos = produtoSelecionado && form.quantidade > 0
    ? produtoSelecionado.estoque_atual + Number(form.quantidade)
    : null;

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Registrar Entrada de Estoque"
          subtitle="Adicione quantidades aos produtos existentes"
        />

        <div className="tipo-controle">
          {["Entrada", "Ajuste"].map((tipo) => (
            <button
              key={tipo}
              className={`tipo-btn ${tipoAtivo === tipo ? "active" : ""}`}
              type="button"
              onClick={() => selecionarTipo(tipo)}
            >
              {tipo}
            </button>
          ))}
        </div>

        {erro && <div className="alert alert-erro">{erro}</div>}
        {sucesso && <div className="alert alert-sucesso">{sucesso}</div>}

        <form className="form-grid" onSubmit={handleSubmit}>
          <select name="produto_id" value={form.produto_id} onChange={handleChange} required>
            <option value="">Selecione o produto *</option>
            {produtos.map((p) => (
              <option key={p.id} value={p.id}>
                {p.nome} — estoque: {p.estoque_atual}
              </option>
            ))}
          </select>

          <div className="input-com-info">
            <input
              type="number"
              name="quantidade"
              placeholder="Quantidade *"
              value={form.quantidade}
              onChange={handleChange}
              min="1"
              required
            />
            {estoqueApos !== null && (
              <span className="estoque-preview">
                Estoque atual: <strong>{produtoSelecionado.estoque_atual}</strong> → após entrada: <strong>{estoqueApos}</strong>
              </span>
            )}
          </div>

          <select name="sub_tipo" value={form.sub_tipo} onChange={handleChange}>
            {opcoesSubTipo.map((op) => (
              <option key={op} value={op}>{op}</option>
            ))}
          </select>

          <input
            type="number"
            name="custo_unitario"
            placeholder="Custo unitário (opcional)"
            value={form.custo_unitario}
            onChange={handleChange}
            min="0"
            step="0.01"
          />

          {mostrarFornecedor && (
            <select
              name="fornecedor_id"
              value={form.fornecedor_id}
              onChange={handleChange}
              className="full-input"
            >
              <option value="">Fornecedor (opcional)</option>
              {fornecedores.map((f) => (
                <option key={f.id} value={f.id}>{f.nome}</option>
              ))}
            </select>
          )}

          <textarea
            name="observacoes"
            placeholder="Observações"
            value={form.observacoes}
            onChange={handleChange}
          />

          <button className="btn-submit" type="submit" disabled={carregando}>
            {carregando ? "Registrando..." : "Registrar entrada"}
          </button>
        </form>
      </div>

      {historico.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <h3 style={{ marginBottom: "1rem", color: "#111827" }}>Últimas entradas</h3>
          <table>
            <thead>
              <tr>
                <th>Produto</th>
                <th>Qtd</th>
                <th>Tipo</th>
                <th>Motivo</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody>
              {historico.map((m) => (
                <tr key={m.id}>
                  <td>{m.nome_produto || `#${m.produto_id}`}</td>
                  <td>+{m.quantidade}</td>
                  <td>{m.tipo_movimentacao?.replace("ENTRADA_", "").toLowerCase()}</td>
                  <td>{m.motivo || "—"}</td>
                  <td>{new Date(m.criado_em).toLocaleString("pt-BR")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default EntradaEstoque;

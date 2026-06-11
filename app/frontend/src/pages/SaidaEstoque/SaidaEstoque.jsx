import { useState, useEffect } from "react";
import PageHeader from "../../components/PageHeader/PageHeader";
import { produtosAPI, estoqueAPI } from "../../service/api";
import "./SaidaEstoque.css";

const TIPO_MAP = {
  Venda: "SAIDA_VENDA",
  Saída: "SAIDA_BAIXA",
  Ajuste: "SAIDA_AJUSTE",
  Perda: "SAIDA_BAIXA",
};

const MOTIVOS = {
  Venda: ["Venda"],
  Saída: ["Uso interno", "Retirada interna"],
  Ajuste: ["Ajuste de inventário", "Correção de estoque"],
  Perda: ["Produto danificado", "Produto vencido", "Perda"],
};

const FORM_INICIAL = {
  produto_id: "",
  quantidade: "",
  motivo: "Venda",
  responsavel: "",
  observacoes: "",
};

function SaidaEstoque() {
  const [tipoAtivo, setTipoAtivo] = useState("Venda");
  const [form, setForm] = useState({ ...FORM_INICIAL, motivo: "Venda" });
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [historico, setHistorico] = useState([]);

  useEffect(() => {
    carregarProdutos();
    carregarHistorico();
  }, []);

  async function carregarProdutos() {
    try {
      const lista = await produtosAPI.listar({ ativo: true });
      setProdutos(lista);
    } catch {
      setErro("Não foi possível carregar os produtos.");
    }
  }

  async function carregarHistorico() {
    try {
      const lista = await estoqueAPI.historico({ limit: 20 });
      setHistorico(lista.filter((m) => m.direcao === "SAIDA").slice(0, 10));
    } catch {
      // silencioso
    }
  }

  function selecionarTipo(tipo) {
    setTipoAtivo(tipo);
    const primeiroMotivo = MOTIVOS[tipo][0];
    setForm((f) => ({ ...f, motivo: primeiroMotivo }));
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

    setCarregando(true);
    try {
      const payload = {
        produto_id: Number(form.produto_id),
        tipo_movimentacao: TIPO_MAP[tipoAtivo],
        quantidade: Number(form.quantidade),
        motivo: form.motivo || null,
        ...(form.responsavel && { documento_referencia: form.responsavel }),
      };

      await estoqueAPI.registrarSaida(payload);
      const nomeProduto =
        produtos.find((p) => p.id === Number(form.produto_id))?.nome ||
        `Produto #${payload.produto_id}`;
      setSucesso(`Saída de ${payload.quantidade} unidade(s) de "${nomeProduto}" registrada!`);
      setForm({ ...FORM_INICIAL, motivo: MOTIVOS[tipoAtivo][0] });
      carregarProdutos();
      carregarHistorico();
    } catch (err) {
      setErro(err.message);
    } finally {
      setCarregando(false);
    }
  }

  const produtoSelecionado = produtos.find((p) => p.id === Number(form.produto_id));

  return (
    <section>
      <div className="page-card">
        <PageHeader
          title="Registrar Saída de Estoque"
          subtitle="Registre vendas, perdas ou retiradas internas"
        />

        <div className="tipo-controle">
          {Object.keys(MOTIVOS).map((tipo) => (
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
                {p.nome} — estoque: {p.estoque_atual} {p.unidade_medida}
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
              max={produtoSelecionado?.estoque_atual || undefined}
              required
            />
            {produtoSelecionado && (
              <span className="estoque-hint">
                Disponível: {produtoSelecionado.estoque_atual} {produtoSelecionado.unidade_medida}
              </span>
            )}
          </div>

          <select name="motivo" value={form.motivo} onChange={handleChange}>
            {MOTIVOS[tipoAtivo].map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>

          <input
            type="text"
            name="responsavel"
            placeholder="Responsável"
            value={form.responsavel}
            onChange={handleChange}
          />

          <textarea
            name="observacoes"
            placeholder="Observações"
            value={form.observacoes}
            onChange={handleChange}
            className="full-input"
          />

          <button className="btn-submit" type="submit" disabled={carregando}>
            {carregando ? "Registrando..." : "Registrar saída"}
          </button>
        </form>
      </div>

      {/* Histórico recente */}
      {historico.length > 0 && (
        <div className="page-card" style={{ marginTop: "1.5rem" }}>
          <h3 style={{ marginBottom: "1rem", color: "#111827" }}>
            Últimas saídas
          </h3>
          <table>
            <thead>
              <tr>
                <th>Produto</th>
                <th>Qtd</th>
                <th>Motivo</th>
                <th>Responsável</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody>
              {historico.map((m) => (
                <tr key={m.id}>
                  <td>{m.nome_produto || `#${m.produto_id}`}</td>
                  <td>{m.quantidade}</td>
                  <td>{m.motivo}</td>
                  <td>{m.documento_referencia || "—"}</td>
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

export default SaidaEstoque;

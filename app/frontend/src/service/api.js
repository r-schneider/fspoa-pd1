const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (res.status === 204) return null;

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Erro desconhecido" }));
    throw new Error(err.detail || `Erro ${res.status}`);
  }

  return res.json();
}

function toQuery(params) {
  const filtered = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "")
  );
  const q = new URLSearchParams(filtered).toString();
  return q ? `?${q}` : "";
}

// ─── PRODUTOS ────────────────────────────────────────────────

export const produtosAPI = {
  /** @param {{ q?: string, categoria_id?: number, ativo?: boolean, estoque_baixo?: boolean, sem_estoque?: boolean, skip?: number, limit?: number }} params */
  listar: (params = {}) => request(`/produtos${toQuery(params)}`),

  obter: (id) => request(`/produtos/${id}`),

  /** @param {{ nome: string, preco: number, unidade_medida: string, codigo_barras?: string, estoque_minimo?: number, estoque_maximo?: number, preco_custo?: number, descricao?: string, categoria_id?: number }} data */
  criar: (data) => request("/produtos", { method: "POST", body: JSON.stringify(data) }),

  atualizar: (id, data) =>
    request(`/produtos/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  deletar: (id) => request(`/produtos/${id}`, { method: "DELETE" }),
};

// ─── CATEGORIAS ──────────────────────────────────────────────

export const categoriasAPI = {
  listar: (params = {}) => request(`/categorias${toQuery(params)}`),

  obter: (id) => request(`/categorias/${id}`),

  criar: (data) => request("/categorias", { method: "POST", body: JSON.stringify(data) }),

  atualizar: (id, data) =>
    request(`/categorias/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  deletar: (id) => request(`/categorias/${id}`, { method: "DELETE" }),
};

// ─── FORNECEDORES ────────────────────────────────────────────

export const fornecedoresAPI = {
  listar: (params = {}) => request(`/fornecedores${toQuery(params)}`),

  obter: (id) => request(`/fornecedores/${id}`),

  /** @param {{ nome: string, cnpj?: string, telefone?: string, email?: string, endereco?: string }} data */
  cadastrar: (data) => request("/fornecedores", { method: "POST", body: JSON.stringify(data) }),

  atualizar: (id, data) =>
    request(`/fornecedores/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  desativar: (id) => request(`/fornecedores/${id}`, { method: "DELETE" }),

  /** Alterna ativo/inativo usando PUT (backend não tem endpoint dedicado de toggle) */
  alternarAtivo: (id, ativoAtual) =>
    request(`/fornecedores/${id}`, {
      method: "PUT",
      body: JSON.stringify({ ativo: !ativoAtual }),
    }),
};

// ─── ESTOQUE ─────────────────────────────────────────────────

export const estoqueAPI = {
  /**
   * @param {{ produto_id: number, tipo_movimentacao: "ENTRADA_COMPRA"|"ENTRADA_DEVOLUCAO"|"ENTRADA_AJUSTE", quantidade: number, custo_unitario?: number, motivo?: string, documento_referencia?: string, fornecedor_id?: number }} data
   */
  registrarEntrada: (data) =>
    request("/estoque/entrada", { method: "POST", body: JSON.stringify(data) }),

  /**
   * @param {{ produto_id: number, tipo_movimentacao: "SAIDA_VENDA"|"SAIDA_BAIXA"|"SAIDA_AJUSTE", quantidade: number, preco_unitario?: number, motivo?: string, documento_referencia?: string }} data
   */
  registrarSaida: (data) =>
    request("/estoque/saida", { method: "POST", body: JSON.stringify(data) }),

  /** @param {{ produto_id?: number, tipo_movimentacao?: string, data_inicio?: string, data_fim?: string, skip?: number, limit?: number }} params */
  historico: (params = {}) => request(`/estoque/historico${toQuery(params)}`),

  historicoProduto: (produtoId, params = {}) =>
    request(`/estoque/historico/${produtoId}${toQuery(params)}`),
};

// ─── DASHBOARD ───────────────────────────────────────────────

export const dashboardAPI = {
  completo: () => request("/dashboard"),

  metricas: () => request("/dashboard/metricas"),

  alertas: () => request("/dashboard/alertas"),

  maisVendidos: (limit = 10) => request(`/dashboard/mais-vendidos?limit=${limit}`),

  maisComprados: (limit = 10) => request(`/dashboard/mais-comprados?limit=${limit}`),

  movimentosPorDia: (dias = 7) => request(`/dashboard/movimentos-por-dia?dias=${dias}`),

  estoquePorCategoria: () => request("/dashboard/estoque-por-categoria"),
};

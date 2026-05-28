// Centraliza as chamadas à API do backend
const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Erro desconhecido" }));
    throw new Error(err.detail || `Erro ${res.status}`);
  }

  return res.json();
}

// ─── FORNECEDORES ────────────────────────────────────────────

export const fornecedoresAPI = {
  listar: () => request("/fornecedores/"),

  cadastrar: (data) =>
    request("/fornecedores/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  atualizar: (id, data) =>
    request(`/fornecedores/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  desativar: (id) =>
    request(`/fornecedores/${id}`, { method: "DELETE" }),
};

// ─── SAÍDA DE ESTOQUE ────────────────────────────────────────

export const saidaAPI = {
  listarProdutos: () => request("/saidas/produtos"),

  registrar: (data) =>
    request("/saidas/", {
      method: "POST",
      body: JSON.stringify({ ...data, tipo: "SAIDA" }),
    }),

  listar: () => request("/saidas/"),
};

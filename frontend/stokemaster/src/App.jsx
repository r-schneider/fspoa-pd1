import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar/Sidebar";
import Topbar from "./components/Topbar/Topbar";

import Dashboard from "./pages/Dashboard/Dashboard";
import CadastroProduto from "./pages/CadastroProduto/CadastroProduto";
import EntradaEstoque from "./pages/EntradaEstoque/EntradaEstoque";
import SaidaEstoque from "./pages/SaidaEstoque/SaidaEstoque";
import VisualizarEstoque from "./pages/VisualizarEstoque/VisualizarEstoque";
import CadastroFornecedor from "./pages/CadastroFornecedor/CadastroFornecedor";
import RelatorioMovimentacao from "./pages/RelatorioMovimentacao/RelatorioMovimentacao";
import ProdutosMaisVendidos from "./pages/ProdutosMaisVendidos/ProdutosMaisVendidos";
import AlertaEstoqueBaixo from "./pages/AlertaEstoqueBaixo/AlertaEstoqueBaixo";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  function toggleSidebar() {
    setSidebarOpen(!sidebarOpen);
  }

  return (
    <BrowserRouter>
      <div className={sidebarOpen ? "app" : "app sidebar-collapsed"}>
        <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

        <main className="main">
          <Topbar />

          <div className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/produtos" element={<CadastroProduto />} />
              <Route path="/entrada" element={<EntradaEstoque />} />
              <Route path="/saida" element={<SaidaEstoque />} />
              <Route path="/estoque" element={<VisualizarEstoque />} />
              <Route path="/fornecedores" element={<CadastroFornecedor />} />
              <Route path="/relatorios" element={<RelatorioMovimentacao />} />
              <Route path="/mais-vendidos" element={<ProdutosMaisVendidos />} />
              <Route path="/estoque-baixo" element={<AlertaEstoqueBaixo />} />
            </Routes>
          </div>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

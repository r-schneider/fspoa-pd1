import { useState } from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import Sidebar from "./components/Sidebar/Sidebar";
import Topbar from "./components/Topbar/Topbar";

import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import CadastroProduto from "./pages/CadastroProduto/CadastroProduto";
import EntradaEstoque from "./pages/EntradaEstoque/EntradaEstoque";
import SaidaEstoque from "./pages/SaidaEstoque/SaidaEstoque";
import VisualizarEstoque from "./pages/VisualizarEstoque/VisualizarEstoque";
import CadastroFornecedor from "./pages/CadastroFornecedor/CadastroFornecedor";
import RelatorioMovimentacao from "./pages/RelatorioMovimentacao/RelatorioMovimentacao";
import ProdutosMaisVendidos from "./pages/ProdutosMaisVendidos/ProdutosMaisVendidos";
import AlertaEstoqueBaixo from "./pages/AlertaEstoqueBaixo/AlertaEstoqueBaixo";

function AppContent() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const isLoginPage = location.pathname === "/login";

  function toggleSidebar() {
    setSidebarOpen(!sidebarOpen);
  }

  if (isLoginPage) {
    return <Login />;
  }

  return (
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
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={<AppContent />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

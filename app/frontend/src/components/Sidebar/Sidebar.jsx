import { NavLink } from "react-router-dom";
import {
  FaChartLine,
  FaBox,
  FaArrowDown,
  FaArrowUp,
  FaTableCells,
  FaTruck,
  FaFileLines,
  FaRankingStar,
  FaTriangleExclamation,
  FaChevronLeft,
  FaChevronRight,
  FaTag,
} from "react-icons/fa6";

import "./Sidebar.css";

function Sidebar({ sidebarOpen, toggleSidebar }) {
  return (
    <aside className={sidebarOpen ? "sidebar" : "sidebar collapsed"}>
      <div>
        <div className="logo">
          <div className="logo-icon">
            <FaBox />
          </div>

          {sidebarOpen && <h1>Stockmaster</h1>}

          <button className="sidebar-toggle" onClick={toggleSidebar}>
            {sidebarOpen ? <FaChevronLeft /> : <FaChevronRight />}
          </button>
        </div>

        <nav className="menu">
          {sidebarOpen && <p className="menu-title">Visão geral</p>}

          <NavLink to="/" end className="menu-item">
            <FaChartLine />
            {sidebarOpen && <span>Dashboard</span>}
          </NavLink>

          {sidebarOpen && <p className="menu-title">Estoque</p>}
          {!sidebarOpen && <div className="menu-separator" />}

          <NavLink to="/estoque" className="menu-item">
            <FaTableCells />
            {sidebarOpen && <span>Visualizar estoque</span>}
          </NavLink>

          <NavLink to="/entrada" className="menu-item">
            <FaArrowDown />
            {sidebarOpen && <span>Entrada de estoque</span>}
          </NavLink>

          <NavLink to="/saida" className="menu-item">
            <FaArrowUp />
            {sidebarOpen && <span>Saída de estoque</span>}
          </NavLink>

          {sidebarOpen && <p className="menu-title">Cadastros</p>}
          {!sidebarOpen && <div className="menu-separator" />}

          <NavLink to="/produtos" className="menu-item">
            <FaBox />
            {sidebarOpen && <span>Produtos</span>}
          </NavLink>

          <NavLink to="/categorias" className="menu-item">
            <FaTag />
            {sidebarOpen && <span>Categorias</span>}
          </NavLink>

          <NavLink to="/fornecedores" className="menu-item">
            <FaTruck />
            {sidebarOpen && <span>Fornecedores</span>}
          </NavLink>

          {sidebarOpen && <p className="menu-title">Relatórios</p>}
          {!sidebarOpen && <div className="menu-separator" />}

          <NavLink to="/relatorios" className="menu-item">
            <FaFileLines />
            {sidebarOpen && <span>Movimentações</span>}
          </NavLink>

          <NavLink to="/mais-vendidos" className="menu-item">
            <FaRankingStar />
            {sidebarOpen && <span>Análise de vendas</span>}
          </NavLink>

          <NavLink to="/estoque-baixo" className="menu-item">
            <FaTriangleExclamation />
            {sidebarOpen && <span>Alertas de estoque</span>}
          </NavLink>
        </nav>
      </div>

      <div className="user-box">
        <div className="avatar"></div>

        {sidebarOpen && (
          <div>
            <strong>Usuário Admin</strong>
            <span>Front-end</span>
          </div>
        )}
      </div>
    </aside>
  );
}

export default Sidebar;

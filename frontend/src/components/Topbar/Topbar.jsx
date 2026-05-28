import { FaBell, FaMagnifyingGlass, FaPlus } from "react-icons/fa6";
import "./Topbar.css";

function Topbar() {
  return (
    <header className="topbar">
      <div className="topbar-title">
        <h2>Stockmaster</h2>
        <p>Sistema de gerenciamento de estoque</p>
      </div>

      <div className="topbar-actions">
        <div className="search-box">
          <FaMagnifyingGlass />
          <input type="text" placeholder="Pesquisar..." />
        </div>

        <button className="topbar-button">
          <FaPlus />
          Novo item
        </button>

        <button className="notification">
          <FaBell />
          <span></span>
        </button>
      </div>
    </header>
  );
}

export default Topbar;

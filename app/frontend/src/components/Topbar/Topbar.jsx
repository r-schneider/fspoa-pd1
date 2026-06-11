import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaBell, FaMagnifyingGlass, FaPlus } from "react-icons/fa6";
import { dashboardAPI } from "../../service/api";
import "./Topbar.css";

function Topbar() {
  const navigate = useNavigate();
  const [busca, setBusca] = useState("");
  const [alertasCount, setAlertasCount] = useState(0);

  useEffect(() => {
    dashboardAPI.metricas()
      .then((m) => setAlertasCount((m.estoque_baixo || 0) + (m.sem_estoque || 0)))
      .catch(() => {});
  }, []);

  function handleBuscaKeyDown(e) {
    if (e.key === "Enter" && busca.trim()) {
      navigate(`/estoque?q=${encodeURIComponent(busca.trim())}`);
    }
  }

  return (
    <header className="topbar">
      <div className="topbar-title">
        <h2>Stockmaster</h2>
        <p>Sistema de gerenciamento de estoque</p>
      </div>

      <div className="topbar-actions">
        <div className="search-box">
          <FaMagnifyingGlass />
          <input
            type="text"
            placeholder="Pesquisar produto... (Enter)"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            onKeyDown={handleBuscaKeyDown}
          />
        </div>

        <button className="topbar-button" onClick={() => navigate("/produtos")}>
          <FaPlus />
          Novo produto
        </button>

        <button
          className="notification"
          onClick={() => navigate("/estoque-baixo")}
          title={`${alertasCount} produto(s) com estoque baixo`}
        >
          <FaBell />
          {alertasCount > 0 && <span className="notif-badge">{alertasCount > 9 ? "9+" : alertasCount}</span>}
        </button>
      </div>
    </header>
  );
}

export default Topbar;

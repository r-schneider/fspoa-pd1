import "./StatusBadge.css";

function StatusBadge({ status }) {
  function getClassName() {
    if (status === "Crítico") return "critico";
    if (status === "Atenção") return "atencao";
    if (status === "Entrada") return "entrada";
    if (status === "Saída") return "saida";
    if (status === "Ajuste") return "ajuste";
    return "estavel";
  }

  return <span className={`status-badge ${getClassName()}`}>{status}</span>;
}

export default StatusBadge;

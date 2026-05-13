import "./CardMetric.css";

function CardMetric({ title, value, description, icon, color = "blue", danger }) {
  return (
    <div className="card-metric">
      <div>
        <p>{title}</p>
        <h3>{value}</h3>
        <span className={danger ? "danger" : ""}>{description}</span>
      </div>

      <div className={`card-metric-icon ${color}`}>{icon}</div>
    </div>
  );
}

export default CardMetric;

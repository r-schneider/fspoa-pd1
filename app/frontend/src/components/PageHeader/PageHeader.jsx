import "./PageHeader.css";

function PageHeader({ title, subtitle, buttonText, onButtonClick }) {
  return (
    <div className="page-header">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>

      {buttonText && (
        <button className="btn-light" onClick={onButtonClick}>
          {buttonText}
        </button>
      )}
    </div>
  );
}

export default PageHeader;

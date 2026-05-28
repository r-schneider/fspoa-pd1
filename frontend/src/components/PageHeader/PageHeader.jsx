import "./PageHeader.css";

function PageHeader({ title, subtitle, buttonText }) {
  return (
    <div className="page-header">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>

      {buttonText && <button className="btn-light">{buttonText}</button>}
    </div>
  );
}

export default PageHeader;

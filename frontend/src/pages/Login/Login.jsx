import { useState } from "react";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [modalAberto, setModalAberto] = useState(false);
  const [emailRecuperacao, setEmailRecuperacao] = useState("");
  const [mensagem, setMensagem] = useState("");

  function fazerLogin(event) {
    event.preventDefault();

    if (email && senha) {
      alert("Login realizado com sucesso!");
      window.location.href = "/";
    }
  }

  function enviarRecuperacao() {
    if (!emailRecuperacao) {
      setMensagem("Digite um e-mail válido.");
      return;
    }

    setMensagem("E-mail de recuperação enviado com sucesso!");
  }

  function fecharModal() {
    setModalAberto(false);
    setEmailRecuperacao("");
    setMensagem("");
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo-area">
          <div className="login-logo-icon">💼</div>
          <h1>Stockmaster</h1>
          <p>Sistema de gerenciamento de estoque</p>
        </div>

        <form onSubmit={fazerLogin}>
          <div className="login-input-group">
            <label>E-mail</label>
            <input
              type="email"
              placeholder="Digite seu e-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="login-input-group">
            <label>Senha</label>
            <input
              type="password"
              placeholder="Digite sua senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </div>

          <div className="login-options">
            <label>
              <input type="checkbox" />
              Lembrar-me
            </label>

            <button
              type="button"
              onClick={() => setModalAberto(true)}
              className="login-forgot-button"
            >
              Esqueci minha senha
            </button>
          </div>

          <button type="submit" className="login-button">
            Entrar
          </button>
        </form>

        <p className="login-footer-text">Acesso restrito ao administrador</p>
      </div>

      {modalAberto && (
        <div className="login-modal-overlay" onClick={fecharModal}>
          <div className="login-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="login-close-button" onClick={fecharModal}>
              &times;
            </button>

            <h2>Recuperar senha</h2>

            <p>
              Informe seu e-mail para receber as instruções de redefinição de
              senha.
            </p>

            <input
              type="email"
              placeholder="Digite seu e-mail"
              value={emailRecuperacao}
              onChange={(e) => setEmailRecuperacao(e.target.value)}
            />

            <button className="login-button" onClick={enviarRecuperacao}>
              Enviar e-mail
            </button>

            {mensagem && (
              <small
                className={
                  mensagem.includes("válido")
                    ? "login-message-error"
                    : "login-message-success"
                }
              >
                {mensagem}
              </small>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Login;

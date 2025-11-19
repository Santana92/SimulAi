// --- Bloco de Importação ---
import GoogleIcon from "../../assets/google-icon.png";
import LeBudda from "../../assets/LeBudda.png";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PopupCadastro from "./PopupCadastro";
import { useGoogleLogin } from '@react-oauth/google';

// --- Componente Login ---
// Componente que renderiza a página de login, permitindo autenticação
// via email/senha ou Google.
const Login = () => {
    // --- Estados do Componente ---
    const [isPopupOpen, setIsPopupOpen] = useState(false); // Controla a visibilidade do popup de cadastro.
    const [email, setEmail] = useState(""); // Armazena o email digitado.
    const [senha, setSenha] = useState(""); // Armazena a senha digitada.
    const [usuarioLogado, setUsuarioLogado] = useState(null); // Armazena os dados do usuário após o login.

    // --- Hooks ---
    const navigate = useNavigate(); // Hook para navegação entre as páginas.

    // --- Efeito para Redirecionamento ---
    // Executa sempre que o estado 'usuarioLogado' muda.
    useEffect(() => {
        // Se o login for bem-sucedido, redireciona o usuário para o dashboard correto.
        if (usuarioLogado) {
            if (usuarioLogado.tipo === "aluno") {
                navigate("/aluno");
            } else if (usuarioLogado.tipo === "professor") {
                navigate("/professor");
            }
        }
    }, [usuarioLogado, navigate]);

    // --- Funções de Manipulação de Eventos ---
    const openPopup = () => {
        setIsPopupOpen(true);
    };

    // --- Lógica de Login com Google ---
    const handleGoogleLoginSuccess = async (tokenResponse) => {
        const code = tokenResponse.code;
        try {
            // Envia o código de autorização para o backend.
            const response = await fetch('http://127.0.0.1:8000/auth/google', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha no login com Google');
            }

            // Se o login for bem-sucedido, armazena os dados do usuário.
            const usuario = await response.json();
            localStorage.setItem('userId', usuario.id);
            localStorage.setItem('userType', usuario.tipo);
            localStorage.setItem('userName', usuario.nome);
            setUsuarioLogado(usuario); // Dispara o redirecionamento.

        } catch (error) {
            console.error("Erro no login com Google:", error);
            alert(`Não foi possível fazer login com o Google: ${error.message}`);
        }
    };

    // Configuração do hook de login do Google.
    const googleLogin = useGoogleLogin({
        flow: 'auth-code', // Usa o fluxo de código de autorização.
        onSuccess: handleGoogleLoginSuccess,
        onError: (error) => {
            console.error('Login com Google falhou:', error);
            alert('Ocorreu um erro durante o login com Google.');
        }
    });

    // --- Lógica de Login com Email/Senha ---
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            // Envia email e senha para o backend.
            const response = await fetch('http://127.0.0.1:8000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, senha: senha }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha no login');
            }

            // Se o login for bem-sucedido, armazena os dados do usuário.
            const usuario = await response.json();
            localStorage.setItem('userId', usuario.id);
            localStorage.setItem('userType', usuario.tipo);
            localStorage.setItem('userName', usuario.nome);
            setUsuarioLogado(usuario); // Dispara o redirecionamento.

        } catch (error) {
            console.error("Erro no login:", error);
            alert(error.message);
        }
    };

    // --- Lógica de Cadastro ---
    const handleCadastro = async (usuario, tipo) => {
        const novoUsuario = { ...usuario, tipo: tipo };
        try {
            // Envia os dados do novo usuário para o backend.
            const response = await fetch('http://127.0.0.1:8000/usuarios', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoUsuario),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha ao cadastrar usuário');
            }

            await response.json();
            alert("Cadastro realizado com sucesso! Por favor, faça o login.");
            setIsPopupOpen(false); // Fecha o popup.

        } catch (error) {
            console.error("Erro no cadastro:", error);
            alert(`Não foi possível cadastrar: ${error.message}`);
        }
    };

    // --- Renderização do Componente ---
    return (
        <div className="login-page-wrapper">
            <main className="login-container">
                <div className="login-box">
                    <div className="login-form-area">
                        <div className="login-header">
                            <h2>BEM VINDO DE VOLTA!</h2>
                            <p>Por favor, insira seu email e senha.</p>
                        </div>

                        {/* Formulário de login padrão */}
                        <form className="login-form" onSubmit={handleLogin}>
                            <div className="input-group">
                                <label htmlFor="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    name="email"
                                    placeholder="Digite seu email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="input-group">
                                <label htmlFor="password">Senha</label>
                                <input
                                    type="password"
                                    id="password"
                                    name="password"
                                    placeholder="Digite sua senha"
                                    value={senha}
                                    onChange={(e) => setSenha(e.target.value)}
                                    required
                                />
                            </div>
                            <button type="submit" className="btn primary-btn">
                                Entrar
                            </button>
                        </form>

                        <div className="divider">ou</div>

                        {/* Botão de login com Google */}
                        <button
                            type="button"
                            className="btn google-btn"
                            onClick={() => googleLogin()}
                        >
                            <img src={GoogleIcon} alt="Google logo" />
                            Entrar com Google
                        </button>

                        {/* Link para abrir o popup de cadastro */}
                        <div style={{ marginTop: "20px", textAlign: "center" }}>
                            <a href="#" onClick={openPopup}>
                                Não tem conta? Cadastre-se aqui.
                            </a>
                        </div>
                    </div>

                    {/* Área da imagem lateral */}
                    <div className="login-image-area">
                        <img src={LeBudda} alt="LeBudda" />
                    </div>
                </div>

                {/* Renderiza o popup de cadastro se isPopupOpen for true */}
                {isPopupOpen && (
                    <PopupCadastro
                        onClose={() => setIsPopupOpen(false)}
                        onConfirm={handleCadastro}
                    />
                )}
            </main>
        </div>
    );
};

export default Login;

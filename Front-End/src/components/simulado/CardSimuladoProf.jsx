// src/components/CardSimulado.jsx

import { useState } from "react";
// Importa o hook para navegação
import { useNavigate } from "react-router-dom";
// Importa as imagens que você usou no SimuladoItem (se quiser usá-las)
import ClipboardTeste from '../../assets/ClipboardTeste.png';
import MedalTeste from '../../assets/MedalTeste.png';
import CardAluno from "../professor/CardAluno";

// Componente para exibir um item de simulado com opções de ação.
export default function CardSimuladoProf({ simulado, resultados = []}) {
  const [aberto, setAberto] = useState(false);
  // Inicializa o hook de navegação
  const navigate = useNavigate();
  console.log("📘 Resultados recebidos para", simulado.nome, resultados);

  // Função para navegar para a página de realização do simulado
  const handleRealizarSimulado = () => {
    // Navega para a rota /simulado/:id (passando o ID do simulado na URL)
    navigate(`/simulado/${simulado.id}`);
  };

  // Função para navegar para a página de resultados/feedback
  const handleVerResultado = () => {
    // Navega para a rota /feedback/:id (passando o ID do simulado na URL)
    // TODO: Adicionar lógica para saber se o aluno já fez o simulado
    navigate(`/feedback/${simulado.id}`);
  };

  return (
    <div className="simulado-item"> {/* Mantém a classe para estilo */}
      {/* A área principal do simulado é clicável e alterna o estado 'aberto'. */}
      <div className="simulado" onClick={() => setAberto(!aberto)}>
        {/* Ícone de seta */}
        <span className={`material-icons arrow ${aberto ? "open" : ""}`}>
          chevron_right
        </span>
        {/* Título do simulado */}
        <span className="titulo-simulado">{simulado.nome}</span>
      </div>
      
      {/* Conteúdo com as opções (botões) */}
      {aberto && (
        <div className="simulado-options active">
          
          <div className="lista-alunos">
            {resultados.length > 0 ? (
              resultados.map((aluno) => (
                <CardAluno key={aluno.id} aluno={aluno} />
              ))
            ) : (
              <p style={{ color: "black" }}>
                Nenhum aluno realizou este simulado ainda.
              </p>
            )}
          </div>

          {/* Opção para Realizar o Simulado */}
          <div className="simulado-option-item" onClick={handleRealizarSimulado} style={{ cursor: "pointer" }}>
            <img src={ClipboardTeste} alt="Realizar" />
            <div className="simulado-option-text">
              <h4>Realizar simulado</h4>
              <p>Inicie o simulado e responda às questões.</p>
            </div>
          </div>
          
          {/* Opção para Ver Resultados */}
          {/* TODO: Adicionar lógica para mostrar/esconder este botão */}
          <div className="simulado-option-item" onClick={handleVerResultado} style={{ cursor: "pointer" }}>
            <img src={MedalTeste} alt="Resultados" />
            <div className="simulado-option-text">
              <h4>Ver Resultado</h4>
              <p>Veja seu desempenho e feedback neste simulado.</p>
            </div>
          </div>
          
        </div>
      )}
    </div>
  );
}

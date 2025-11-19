// --- Bloco de Importação ---
import { useState } from 'react';
import ClipboardTeste from '../../assets/ClipboardTeste.png';
import MedalTeste from '../../assets/MedalTeste.png';
import "../../index.css";
import { useNavigate } from "react-router-dom";

// --- Componente SimuladoItem ---
// Renderiza um item de simulado expansível dentro da lista de uma matéria.
const SimuladoItem = ({ simulado, resultado }) => {
  // --- Hooks e Estados ---
  const [aberto, setAberto] = useState(false); // Controla a visibilidade das opções.
  const navigate = useNavigate(); // Hook para navegação.

  // --- Renderização do Componente ---
  return (
    <div className="simulado-item">
      {/* Cabeçalho do item, que expande/recolhe ao ser clicado. */}
      <div className="simulado" onClick={() => setAberto(!aberto)}>
        <span className={`material-icons arrow bolder ${aberto ? 'open' : ''}`}>
          chevron_right
        </span>
        <span className="titulo-simulado">{simulado.nome}</span>
        
        {/* Exibe a nota do simulado ou o status "NÃO REALIZADO". */}
        <div className="simulado-status">
          {resultado ? (
            <span className="nota">NOTA {resultado.nota.toFixed(1)}</span>
          ) : (
            <span className="nao-realizado">NÃO REALIZADO</span>
          )}
        </div>
      </div>

      {/* Opções do simulado, visíveis apenas quando o item está aberto. */}
      {aberto && (
        <div id={simulado.id} className="simulado-options active">
          {/* Opção para realizar o simulado. */}
          <div className="simulado-option-item" onClick={() => navigate(`/simulado/${simulado.id}`)} style={{ cursor: "pointer" }}>
            <img src={ClipboardTeste} alt="clipboard" />
            <div className="simulado-option-text">
              <h4>Realizar simulado</h4>
              <p>Inicie o simulado e respondenda as questões geradas.</p>
            </div>
          </div>
          {/* Opção para ver os resultados/feedback. */}
          <div className="simulado-option-item" onClick={() => navigate(`/feedback/${simulado.id}`)} style={{ cursor: "pointer" }}>
            <img src={MedalTeste} alt="medal" />
            <div className="simulado-option-text">
              <h4>Resultados do simulado</h4>
              <p>
                Saiba dos resultados obtidos do simulado e pontos que você pode
                melhorar.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SimuladoItem;

// --- Bloco de Importação ---
import { useState } from 'react';
import SimuladoItem from '../simulado/SimuladoItem';

// --- Componente MateriaCard ---
// Renderiza um card expansível para uma matéria, mostrando os simulados associados.
const MateriaCard = ({ materia, resultados }) => {
  // --- Estado do Componente ---
  // Controla se o card está expandido (aberto) ou não.
  const [aberto, setAberto] = useState(false);

  // --- Renderização do Componente ---
  return (
    <div className="card">
      {/* Cabeçalho do card que, ao ser clicado, expande ou recolhe o conteúdo. */}
      <div className="card-header" onClick={() => setAberto(!aberto)}>
        {materia.nome}
        <span className={`material-icons arrow ${aberto ? 'open' : ''}`}>
          chevron_right
        </span>
      </div>
      
      {/* Conteúdo do card, visível apenas quando 'aberto' é true. */}
      {aberto && (
        <div id={materia.id} className="card-content active">
          <div className="grid simulados">
            {/* Mapeia a lista de simulados da matéria. */}
            {materia.simulados.map((simulado) => (
              // Renderiza um item de simulado, passando o resultado correspondente.
              <SimuladoItem 
                key={simulado.id} 
                simulado={simulado} 
                resultado={resultados[simulado.id]} 
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MateriaCard;

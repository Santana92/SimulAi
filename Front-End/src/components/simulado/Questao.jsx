// --- Bloco de Importação ---
import React from "react";

// --- Componente Questao ---
// Renderiza uma única questão de um simulado, com suas opções e feedback.
export default function Questao({ questao, resposta, onResponder, bloqueada }) {
  return (
    // --- Estrutura do Componente ---
    <div className="question">
      <h3>Questão {questao.id}</h3>
      <p>{questao.pergunta}</p>
      
      {/* Container para as opções da questão. */}
      <div className="options">
        {/* Mapeia as opções da questão para renderizar cada uma. */}
        {Object.entries(questao.opcoes).map(([letra, texto]) => {
          // --- Lógica de Estilo das Opções ---
          const selecionada = resposta?.escolha === letra;
          const correta = questao.correta === letra;
          const incorreta = selecionada && resposta?.escolha !== questao.correta;

          return (
            <div
              key={letra}
              // Define as classes CSS com base no estado da resposta.
              className={`option 
                ${selecionada ? "selected" : ""} 
                ${correta && resposta ? "correct" : ""} 
                ${incorreta ? "incorrect" : ""}`}
              // Permite responder apenas se a questão não estiver bloqueada.
              onClick={() => !bloqueada && onResponder(questao.id, letra)}
            >
              {letra}) {texto}
              
              {/* Exibe a explicação apenas após a resposta ser enviada. */}
              {resposta && (correta || incorreta) && (
                <div
                  className={`explanation ${
                    correta ? "correct" : incorreta ? "incorrect" : ""
                  }`}
                >
                  <span className="material-icons">
                    {correta ? "check" : "close"}
                  </span>
                  {questao.explicacoes[letra]}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

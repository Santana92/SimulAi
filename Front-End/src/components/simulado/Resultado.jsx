// --- Bloco de Importação ---
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// --- Componente Resultado ---
// Renderiza a tela de resultado do simulado, mostrando a pontuação,
// o gabarito e salvando o resultado na API.
export default function Resultado({ questoes, respostas, onRestart, simuladoId }) {
  // --- Hooks e Estados ---
  const navigate = useNavigate();
  const [salvo, setSalvo] = useState(false); // Estado para controlar se o resultado já foi salvo.

  // --- Lógica de Cálculo ---
  // Calcula o número de acertos comparando as respostas com o gabarito.
  const acertos = questoes.filter(
    (q) => respostas[q.id]?.escolha === q.correta
  ).length;

  // --- Efeito para Salvar o Resultado ---
  // Executa quando o componente é montado para salvar o resultado na API.
  useEffect(() => {
    const userType = localStorage.getItem('userType');
    // Impede o salvamento se o usuário for um professor ou se o resultado já foi salvo.
    if (userType === 'professor' || salvo) {
      return;
    }

    const salvarResultado = async () => {
      try {
        // Coleta os dados necessários para salvar o resultado.
        const userId = localStorage.getItem('userId');
        const userName = localStorage.getItem('userName');
        const nota = (acertos / questoes.length) * 10;

        // Formata o objeto de respostas para o formato esperado pela API.
        const respostasParaSalvar = Object.entries(respostas).reduce((acc, [id, resp]) => {
          acc[id] = resp.escolha;
          return acc;
        }, {});

        const resultadoData = {
          usuario_id: userId,
          usuario_nome: userName,
          simulado_id: simuladoId,
          nota: nota,
          respostas: respostasParaSalvar
        };

        // Envia os dados para a API.
        const response = await fetch(`http://127.0.0.1:8000/simulados/${simuladoId}/resultados`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(resultadoData),
        });

        if (!response.ok) {
          throw new Error('Erro ao salvar resultado');
        }

        await response.json();
        setSalvo(true); // Marca como salvo para evitar duplicação.

      } catch (error) {
        console.error('Erro ao salvar resultado:', error);
      }
    };

    salvarResultado();
  }, [acertos, questoes.length, respostas, simuladoId, salvo]);

  // --- Funções de Navegação ---
  // Redireciona o usuário para o dashboard correto ao clicar em "Voltar ao Menu".
  const handleVoltarMenu = () => {
    const userType = localStorage.getItem('userType');
    if (userType === 'professor') {
      navigate('/professor');
    } else {
      navigate('/aluno');
    }
  };

  // --- Renderização do Componente ---
  return (
    <div className="resultado-container">
      <h3>Resultado do Simulado</h3>
      <p>
        Você acertou <strong id="acertos">{acertos}</strong> de{" "}
        <strong id="total">{questoes.length}</strong> questões.
      </p>

      {/* Seção do Gabarito */}
      <div id="gabarito">
         {questoes.map((q) => {
          const escolha = respostas[q.id]?.escolha;
          const correta = escolha === q.correta;
          return (
            <p key={q.id} className={correta ? "correct" : "incorrect"}>
              <strong>Questão {q.id}:</strong> {q.pergunta} <br />
              <strong>Sua resposta:</strong> {escolha?.toUpperCase() || "N/A"} |{" "}
              <strong>Resposta correta:</strong> {q.correta.toUpperCase()}
            </p>
          );
        })}
      </div>

      {/* Botões de Ação */}
      <button id="restart-btn" className="btn" onClick={onRestart}>
        Refazer Simulado
      </button>

      <button
        id="back-menu-btn"
        className="btn"
        onClick={handleVoltarMenu}
        style={{ marginTop: '10px', background: '#6c757d' }}
      >
        Voltar ao Menu
      </button>
    </div>
  );
}

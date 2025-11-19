// --- Bloco de Funções Utilitárias ---
// Função para embaralhar aleatoriamente os elementos de um array.
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// --- Bloco de Importação ---
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Questao from "./Questao";
import Resultado from "./Resultado";

// --- Constantes ---
const API_URL = "http://127.0.0.1:8000";

// --- Componente Simulado ---
// Componente principal para a realização de um simulado.
export default function Simulado() {
  // --- Hooks e Estados ---
  const { simuladoId } = useParams(); // Pega o ID do simulado da URL.
  const [simuladoData, setSimuladoData] = useState(null); // Armazena os dados do simulado.
  const [loading, setLoading] = useState(true); // Controla o estado de carregamento.
  const [error, setError] = useState(null); // Armazena erros da API.
  const [current, setCurrent] = useState(0); // Índice da questão atual.
  const [respostas, setRespostas] = useState({}); // Armazena as respostas do usuário.
  const [finalizado, setFinalizado] = useState(false); // Controla se o simulado foi finalizado.

  // --- Efeito para Buscar e Embaralhar o Simulado ---
  useEffect(() => {
    const fetchSimulado = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_URL}/simulados/${simuladoId}`);
        if (!response.ok) {
          throw new Error("Simulado não encontrado ou falha na API");
        }
        const data = await response.json();

        // Lógica para embaralhar as opções de cada questão.
        const questoesEmbaralhadas = data.questoes.map(questao => {
          const letrasOriginais = ['a', 'b', 'c', 'd', 'e'];
          const respostaCorretaOriginal = questao.opcoes[questao.correta];
          const opcoesParaEmbaralhar = letrasOriginais.map(letra => ({
            letraOriginal: letra,
            texto: questao.opcoes[letra],
            explicacao: questao.explicacoes[letra]
          }));

          shuffleArray(opcoesParaEmbaralhar);

          const novasOpcoes = {};
          const novasExplicacoes = {};
          let novaLetraCorreta = '';

          opcoesParaEmbaralhar.forEach((opcao, index) => {
            const novaLetra = letrasOriginais[index];
            novasOpcoes[novaLetra] = opcao.texto;
            novasExplicacoes[novaLetra] = opcao.explicacao;
            if (opcao.texto === respostaCorretaOriginal) {
              novaLetraCorreta = novaLetra;
            }
          });

          return {
            ...questao,
            opcoes: novasOpcoes,
            explicacoes: novasExplicacoes,
            correta: novaLetraCorreta
          };
        });

        setSimuladoData({ ...data, questoes: questoesEmbaralhadas });

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSimulado();
  }, [simuladoId]);

  // --- Funções de Manipulação de Eventos ---
  // Salva a resposta do usuário para uma questão.
  const handleResponder = (id, escolha) => {
    setRespostas({ ...respostas, [id]: { escolha } });
  };

  // Avança para a próxima questão ou finaliza o simulado.
  const handleNext = () => {
    if (simuladoData && current < simuladoData.questoes.length - 1) {
      setCurrent(current + 1);
    } else {
      setFinalizado(true);
    }
  };

  // Reinicia o simulado, buscando os dados novamente para re-embaralhar.
  const handleRestart = () => {
    setRespostas({});
    setCurrent(0);
    setFinalizado(false);
    // A lógica de fetch é repetida para garantir um novo embaralhamento.
    const fetchSimulado = async () => {
        setLoading(true); setError(null);
        try {
             const response = await fetch(`${API_URL}/simulados/${simuladoId}`);
            if (!response.ok) throw new Error("Simulado não encontrado ou falha na API");
            const data = await response.json();
            const questoesEmbaralhadas = data.questoes.map(questao => {
                const letrasOriginais = ['a', 'b', 'c', 'd', 'e'];
                const respostaCorretaOriginal = questao.opcoes[questao.correta];
                const opcoesParaEmbaralhar = letrasOriginais.map(letra => ({ letraOriginal: letra, texto: questao.opcoes[letra], explicacao: questao.explicacoes[letra] }));
                shuffleArray(opcoesParaEmbaralhar);
                const novasOpcoes = {}; const novasExplicacoes = {}; let novaLetraCorreta = '';
                opcoesParaEmbaralhar.forEach((opcao, index) => {
                    const novaLetra = letrasOriginais[index];
                    novasOpcoes[novaLetra] = opcao.texto; novasExplicacoes[novaLetra] = opcao.explicacao;
                    if (opcao.texto === respostaCorretaOriginal) novaLetraCorreta = novaLetra;
                });
                return { ...questao, opcoes: novasOpcoes, explicacoes: novasExplicacoes, correta: novaLetraCorreta };
            });
            setSimuladoData({ ...data, questoes: questoesEmbaralhadas });
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };
    fetchSimulado();
  };

  // --- Renderização Condicional ---
  if (loading) return <div className="container">Carregando simulado...</div>;
  if (error) return <div className="container">Erro: {error}</div>;
  if (!simuladoData) return <div className="container">Nenhum dado de simulado encontrado.</div>;

  const questoes = simuladoData.questoes;

  // --- Renderização Principal ---
  return (
    <main className="simulado-container">
      <div className="simulado-header"><h2>{simuladoData.titulo}</h2></div>
      {!finalizado ? (
        // Se o simulado não foi finalizado, mostra a questão atual.
        <div className="quiz-container">
          <Questao
            questao={questoes[current]}
            resposta={respostas[questoes[current].id]}
            onResponder={handleResponder}
            bloqueada={!!respostas[questoes[current].id]}
          />
          <div className="actions">
            <button id="next-btn" className="btn" onClick={handleNext}>
              {current < questoes.length - 1 ? "Próximo" : "Finalizar"}
            </button>
          </div>
        </div>
      ) : (
        // Se o simulado foi finalizado, mostra a tela de resultado.
        <Resultado
          questoes={questoes}
          respostas={respostas}
          onRestart={handleRestart}
          simuladoId={simuladoId}
        />
      )}
    </main>  
  );
}

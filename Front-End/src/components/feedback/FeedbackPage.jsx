// src/components/FeedbackPage.jsx

import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import Header from "../ui/Header";
import FeedbackCard from "./FeedbackCard";
import Actions from "../ui/Actions";
import "../../index.css";

const API_URL = "http://127.0.0.1:8000";

/**
 * Página de Feedback (Gabarito Comentado).
 * 
 * Busca os dados de um simulado finalizado e exibe cada questão,
 * a resposta correta e a explicação correspondente como forma de feedback.
 */
export default function FeedbackPage() {
  // Pega o ID do simulado da URL para saber qual gabarito buscar.
  const { simuladoId } = useParams();

  // Estado para guardar os dados do gabarito formatado.
  const [feedbackData, setFeedbackData] = useState(null);
  // Estado para controlar o carregamento.
  const [loading, setLoading] = useState(true);
  // Estado para erros.
  const [error, setError] = useState(null);

  // useEffect para buscar os dados do simulado na API.
  useEffect(() => {
    const fetchSimuladoData = async () => {
      setLoading(true);
      try {
        // Busca o simulado completo usando o endpoint existente.
        const response = await fetch(`${API_URL}/simulados/${simuladoId}`);
        if (!response.ok) {
          throw new Error("Não foi possível carregar o gabarito do simulado.");
        }
        const simulado = await response.json();

        // --- Transforma os dados do simulado em um formato de "Feedback" ---
        const itensDeFeedback = simulado.questoes.map((q) => ({
          // O título de cada item de feedback será a própria pergunta.
          titulo: `Questão ${q.id}: ${q.pergunta}`,
          // O texto será a explicação da alternativa correta.
          texto: `Resposta Correta: ${q.correta.toUpperCase()}. Explicação: ${q.explicacoes[q.correta]}`,
        }));

        // Monta o objeto final que o componente FeedbackCard espera.
        const dataFormatada = {
          feedback: {
            titulo: `Gabarito Comentado: ${simulado.titulo}`,
            itens: itensDeFeedback,
          },
        };

        setFeedbackData(dataFormatada);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSimuladoData();
  }, [simuladoId]); // Roda o efeito sempre que o ID do simulado na URL mudar.

  // Renderiza o estado de carregamento.
  if (loading) {
    return (
        <div className="container">
            <Header />
            <p style={{ textAlign: 'center', color: 'white' }}>Carregando gabarito...</p>
        </div>
    );
  }

  // Renderiza o estado de erro.
  if (error) {
    return (
        <div className="container">
            <Header />
            <p style={{ textAlign: 'center', color: 'red' }}>Erro: {error}</p>
        </div>
    );
  }

  // Renderiza se não encontrar dados.
  if (!feedbackData) {
    return <div className="container">Nenhum dado de feedback encontrado.</div>;
  }

  // Renderiza a página com os dados do gabarito.
  return (
    <div className="container">
      <Header />
      <div className="feedback-container">
        {/* O componente AlunoInfo foi removido pois não temos esses dados aqui */}
        <FeedbackCard
          titulo={feedbackData.feedback.titulo}
          itens={feedbackData.feedback.itens}
        />
        {/* Ações, como o botão de voltar. */}
        <Actions onVoltar={() => window.history.back()} />
      </div>
    </div>
  );
}

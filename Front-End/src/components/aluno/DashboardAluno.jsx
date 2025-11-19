// --- Bloco de Importação ---
import React, { useState, useEffect } from 'react';
import Header from '../ui/Header';
import MateriaCard from '../materia/MateriaCard';
import "../../index.css";

// --- Componente DashboardAluno ---
// Componente principal que monta a página do dashboard do aluno.
export default function DashboardAluno() {
  // --- Estados do Componente ---
  const [materias, setMaterias] = useState([]); // Armazena a lista de matérias.
  const [isLoading, setIsLoading] = useState(true); // Controla a exibição do loader.
  const [error, setError] = useState(null); // Armazena mensagens de erro.
  const [resultados, setResultados] = useState({}); // Armazena os resultados dos simulados do aluno.

  // --- Efeito para Carregar Resultados ---
  // Busca os resultados do aluno na API assim que o componente é montado.
  useEffect(() => {
    const carregarResultadosAluno = async () => {
      try {
        const userId = localStorage.getItem('userId'); // Pega o ID do usuário logado.
        if (userId) {
          const response = await fetch(`http://127.0.0.1:8000/resultados/${userId}`);
          if (response.ok) {
            const data = await response.json();
            
            // Transforma o array de resultados em um objeto para fácil acesso.
            const resultadosPorSimulado = {};
            data.forEach(resultado => {
              resultadosPorSimulado[resultado.simulado_id] = resultado;
            });
            
            setResultados(resultadosPorSimulado);
          }
        }
      } catch (error) {
        console.error("Erro ao carregar resultados:", error);
      }
    };

    carregarResultadosAluno();
  }, []); // Array vazio garante que o efeito rode apenas uma vez.

  // --- Efeito para Carregar Matérias ---
  // Busca a lista de matérias na API.
  useEffect(() => {
    const fetchMaterias = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/materias');
        if (!response.ok) {
          throw new Error('Não foi possível buscar os dados das matérias.');
        }
        const data = await response.json();
        setMaterias(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false); // Para de carregar, com ou sem erro.
      }
    };

    fetchMaterias();
  }, []);

  // --- Renderização Condicional ---
  // Exibe uma mensagem de carregamento enquanto os dados são buscados.
  if (isLoading) {
    return (
      <div className="student-dashboard-container">
        <Header />
        <p style={{ textAlign: 'center', color: 'black', fontSize: '1.2rem' }}>Carregando matérias...</p>
      </div>
    );
  }

  // Exibe uma mensagem de erro se a busca falhar.
  if (error) {
    return (
      <div className="student-dashboard-container">
        <Header />
        <p style={{ textAlign: 'center', color: 'red', fontSize: '1.2rem' }}>Erro: {error}</p>
      </div>
    );
  }

  // --- Renderização Principal ---
  // Exibe o cabeçalho e a lista de matérias.
  return (
    <div className="student-dashboard-container">
      <Header />
      {materias.length > 0 ? (
        // Mapeia cada matéria para um componente MateriaCard.
        materias.map((materia) => (
          <MateriaCard 
            key={materia.id} 
            materia={materia} 
            resultados={resultados} // Passa os resultados para o card da matéria.
          />
        ))
      ) : (
        // Mensagem exibida se não houver matérias.
        <p style={{ textAlign: 'center', color: 'black', fontSize: '1.2rem' }}>Nenhuma matéria encontrada.</p>
      )}
    </div>
  );
}

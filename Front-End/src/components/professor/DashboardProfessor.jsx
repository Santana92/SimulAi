// --- Bloco de Importação ---
import { useEffect, useState } from "react";
import Header from "../ui/Header";
import CardMateriaProf from "../materia/CardMateriaProf.jsx";
import PopupMateria from "../materia/PopupMateria";
import PopupSimulado from "../simulado/PopupSimulado";
import { useLocation } from "react-router-dom";
import "../../index.css";

// --- Constantes ---
const API_URL = "http://127.0.0.1:8000";

// --- Componente DashboardProfessor ---
// Componente principal que monta a página do dashboard do professor.
export default function DashboardProfessor() {
  // --- Estados do Componente ---
  const [materias, setMaterias] = useState([]); // Armazena a lista de matérias.
  const [popupMateriaAberto, setPopupMateriaAberto] = useState(false); // Controla a visibilidade do popup de matéria.
  const [popupSimuladoAberto, setPopupSimuladoAberto] = useState(false); // Controla a visibilidade do popup de simulado.
  const [materiaIdSelecionada, setMateriaIdSelecionada] = useState(null); // Armazena o ID da matéria para adicionar um simulado.
  const [resultados, setResultados] = useState({}); // Armazena os resultados de todos os simulados.
  
  // --- Efeito para Carregar Resultados ---
  // Busca todos os resultados de simulados na API.
  useEffect(() => {
    const carregarResultados = async () => {
      try {
        const response = await fetch(`${API_URL}/resultados`);
        if (!response.ok) {
          throw new Error("Falha ao buscar resultados da API");
        }
        const data = await response.json();
        
        // Agrupa os resultados por simulado_id para fácil acesso.
        const resultadosAgrupados = data.reduce((acc, resultado) => {
          const { simulado_id } = resultado;
          if (!acc[simulado_id]) {
            acc[simulado_id] = [];
          }
          acc[simulado_id].push(resultado);
          return acc;
        }, {});

        setResultados(resultadosAgrupados);
      } catch (error) {
        console.error("Erro ao carregar resultados:", error);
      }
    };
    carregarResultados();
  }, []);

  // --- Efeito para Carregar Matérias ---
  // Busca a lista de matérias na API.
  useEffect(() => {
    const carregarMaterias = async () => {
      try {
        const response = await fetch(`${API_URL}/materias`);
        if (!response.ok) {
          throw new Error("Falha ao buscar matérias da API");
        }
        const data = await response.json();
        setMaterias(data);
      } catch (error) {
        console.error(error);
        alert("Não foi possível carregar as matérias.");
      }
    };
    carregarMaterias();
  }, []);

  // --- Funções de Manipulação de Dados ---
  // Adiciona uma nova matéria via API.
  const adicionarMateria = async (nome) => {
    try {
      const response = await fetch(`${API_URL}/materias`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome: nome }),
      });

      if (!response.ok) {
        throw new Error("Falha ao criar matéria");
      }
      
      const novaMateria = await response.json();
      setMaterias([...materias, novaMateria]); // Atualiza o estado com a nova matéria.
      
    } catch (error) {
      console.error(error);
      alert("Não foi possível adicionar a matéria.");
    }
  };

  // Adiciona um novo simulado a uma matéria via API.
  const adicionarSimulado = async (idMateria, nome, arquivo) => {
    const formData = new FormData();
    formData.append("nome_simulado", nome);
    formData.append("arquivo", arquivo);

    try {
      const response = await fetch(`${API_URL}/materias/${idMateria}/simulados`, {
        method: "POST",
        body: formData, 
      });

      if (!response.ok) {
        const erro = await response.json();
        throw new Error(`Falha ao criar simulado: ${erro.detail}`);
      }
      
      const novoSimulado = await response.json();

      // Atualiza o estado para refletir o novo simulado na matéria correta.
      setMaterias(prevMaterias =>
        prevMaterias.map(materia => {
          if (materia.id === idMateria) {
            const infoSimulado = { id: novoSimulado.id, nome: novoSimulado.titulo };
            return {
              ...materia,
              simulados: [...materia.simulados, infoSimulado],
            };
          }
          return materia;
        })
      );
      
      handleFecharPopupSimulado();
      
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  // --- Funções de Controle de UI ---
  // Abre o popup para adicionar um novo simulado.
  const handleAbrirPopupSimulado = (idMateria) => {
    setMateriaIdSelecionada(idMateria);
    setPopupSimuladoAberto(true);
  };

  // Fecha o popup de simulado.
  const handleFecharPopupSimulado = () => {
    setPopupSimuladoAberto(false);
    setMateriaIdSelecionada(null);
  };
  
  // --- Renderização Principal ---
  return (
    <div className="container">
      <Header />

      {/* Mapeia as matérias para renderizar os cards. */}
      {materias.map((materia) => (
        <CardMateriaProf
          key={materia.id}
          materia={materia}
          resultados={resultados} 
          onAdicionarSimulado={() => handleAbrirPopupSimulado(materia.id)}
        />
      ))}

      {/* Botão flutuante para adicionar nova matéria. */}
      <button className="fab" onClick={() => setPopupMateriaAberto(true)}>
        +
      </button>

      {/* Renderização condicional dos popups. */}
      {popupMateriaAberto && (
        <PopupMateria
          onClose={() => setPopupMateriaAberto(false)}
          onConfirm={adicionarMateria}
        />
      )}
      
      {popupSimuladoAberto && (
        <PopupSimulado
          onClose={handleFecharPopupSimulado}
          onConfirm={(nome, arquivo) => adicionarSimulado(materiaIdSelecionada, nome, arquivo)}
        />
      )}
    </div>
  );
}

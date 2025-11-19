// Importa o hook useState do React para gerenciar o estado do componente.
import { useState } from "react";
// Importa os componentes filhos que serão usados dentro do card.
import CardSimuladoProf from "../simulado/CardSimuladoProf";
import AlunosGrid from "../aluno/AlunosGrid";
// Importa o hook useLocation, embora não esteja sendo utilizado neste componente.
import { useLocation } from "react-router-dom";

// DADOS MOCKADOS (PROVISÓRIOS): Lista de alunos para esta matéria.
// Em uma aplicação real, estes dados viriam do estado da aplicação ou de uma API.
const alunosDaMateria = [
  { id: 1, nome: "João" },
  { id: 2, nome: "Maria" },
  { id: 3, nome: "Pedro" },
];

// Componente para exibir um card de uma matéria, que pode ser expandido.
export default function CardMateriaProf({ materia, onAdicionarSimulado, resultados = {}}) {
  // Estado para controlar se o card está aberto (expandido) ou fechado.
  const [aberto, setAberto] = useState(false);

  // Função placeholder para quando o botão de adicionar aluno for clicado.
  const onAdicionarAluno = () => {
    console.log("Adicionar novo aluno à matéria:", materia.nome);
  };

  return (
    <div className="card">
      {/* O cabeçalho do card é clicável e alterna o estado 'aberto'. */}
      <div className="card-header" onClick={() => setAberto(!aberto)}>
        {materia.nome}
        {/* Ícone de seta que gira com base no estado 'aberto'. */}
        <span className={`material-icons arrow ${aberto ? "open" : ""}`}>
          chevron_right
        </span>
      </div>
      {/* O conteúdo do card só é renderizado se o estado 'aberto' for verdadeiro. */}
      {aberto && (
        <div className="card-content active">
          {/* Mapeia a lista de simulados da matéria e renderiza um CardSimulado para cada um. */}
          {materia.simulados.map((s) => (
            <CardSimuladoProf key={s.id} simulado={s} resultados={resultados[s.id] || []}/>
          ))}
          {/* Botão para adicionar um novo simulado, que chama a função passada por props. */}
          <button className="btn" onClick={onAdicionarSimulado}>
            Adicionar novo simulado
          </button>
          {/* Renderiza a grade de alunos para esta matéria. */}
          <AlunosGrid alunos={alunosDaMateria} onAdicionarAluno={onAdicionarAluno} />
        </div>
      )}
    </div>
  );
}

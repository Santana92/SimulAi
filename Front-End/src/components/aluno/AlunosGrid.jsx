// Importa a imagem padrão do avatar.
import Avatar from "../../assets/Avatar.png";

// Componente para exibir uma grade de avatares de alunos.
export default function AlunosGrid({ alunos, onAdicionarAluno }) {
  return (
    // Container principal para a grade de alunos.
    <div className="grid alunos">
      {/* Container para os ícones dos usuários (avatares). */}
      <div className="user-icons">
        {/* Mapeia a lista de alunos recebida via props. */}
        {alunos.map((aluno) => (
          // Renderiza a imagem do avatar para cada aluno.
          <img
            key={aluno.id} // Chave única para cada elemento da lista.
            src={Avatar} // Usa a imagem de avatar padrão.
            className="avatar aluno"
            alt={`Avatar de ${aluno.nome}`}
          />
        ))}
        {/* Botão para adicionar um novo aluno, que aciona a função recebida via props. */}
        <button
          className="adicionar aluno"
          type="button"
          aria-label="Adicionar aluno"
          onClick={onAdicionarAluno}
        >
          +
        </button>
      </div>
    </div>
  );
}

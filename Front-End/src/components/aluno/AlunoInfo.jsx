// --- Bloco de Importação ---
// Importa a imagem padrão do avatar para ser usada no perfil do aluno.
import Avatar from "../../assets/Avatar.png";

// --- Componente AlunoInfo ---
// Componente funcional que renderiza as informações básicas de um aluno,
// como avatar, nome e ID.
export default function AlunoInfo({ nome, id }) {
  return (
    // --- Estrutura do Componente ---
    // Container principal que agrupa as informações do aluno.
    <div className="aluno-info">
      {/* Mostra o avatar do aluno. */}
      <img src={Avatar} alt="Avatar do Aluno" className="aluno-avatar" />
      
      {/* Container para os dados textuais do aluno. */}
      <div className="aluno-dados">
        {/* Exibe o nome do aluno recebido via props. */}
        <h2>{nome}</h2>
        
        {/* Exibe o ID do aluno recebido via props. */}
        <p>ID: {id}</p>
      </div>
    </div>
  );
}

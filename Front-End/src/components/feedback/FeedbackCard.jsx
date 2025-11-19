// --- Bloco de Importação ---
// Importa o componente filho que será usado para renderizar cada item de feedback.
import FeedbackItem from "./FeedbackItem";

// --- Componente FeedbackCard ---
// Componente que renderiza um card de feedback, agrupando vários itens de feedback
// sob um título comum.
export default function FeedbackCard({ titulo, itens }) {
  return (
    // --- Estrutura do Componente ---
    // Container principal do card de feedback.
    <div className="feedback-card">
      {/* Cabeçalho do card, que exibe o título. */}
      <div className="feedback-header">
        <h3>{titulo}</h3>
      </div>
      
      {/* Corpo do card, que contém a lista de itens de feedback. */}
      <div className="feedback-body">
        {/* Mapeia a lista de 'itens' recebida via props. */}
        {itens.map((item, index) => (
          // Para cada item, renderiza um componente FeedbackItem.
          <FeedbackItem key={index} titulo={item.titulo} texto={item.texto} />
        ))}
      </div>
    </div>
  );
}

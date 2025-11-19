// --- Componente FeedbackItem ---
// Componente funcional que renderiza um único item de feedback, 
// consistindo de um título e um texto descritivo.
export default function FeedbackItem({ titulo, texto }) {
  return (
    // --- Estrutura do Componente ---
    // Container para o item de feedback.
    <div className="feedback-item">
      {/* Exibe o título do feedback. */}
      <h4>{titulo}</h4>
      
      {/* Exibe o texto descritivo do feedback. */}
      <p>{texto}</p>
    </div>
  );
}

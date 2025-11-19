// --- Componente Actions ---
// Componente funcional que renderiza um conjunto de botões de ação, 
// como o botão "Voltar".
export default function Actions({ onVoltar }) {
  return (
    // --- Estrutura do Componente ---
    // Container para os botões de ação.
    <div className="actions">
      {/* Botão que, ao ser clicado, aciona a função onVoltar recebida via props. */}
      <button className="btn" onClick={onVoltar}>Voltar</button>
    </div>
  );
}

// Importa o hook useState do React para gerenciar o estado do formulário.
import { useState } from "react";

// Componente para o popup de adição de uma nova matéria.
export default function PopupMateria({ onClose, onConfirm }) {
  // Estado para armazenar o nome da matéria inserido no campo de texto.
  const [nome, setNome] = useState("");

  // Função chamada ao clicar no botão de confirmação.
  const handleConfirm = () => {
    // Verifica se o campo 'nome' não está vazio.
    if (nome.trim()) {
      // Chama a função onConfirm (passada via props) com o nome da nova matéria.
      onConfirm(nome);
      // Limpa o campo do formulário.
      setNome("");
      // Fecha o popup.
      onClose();
    }
  };

  return (
    // O overlay escurece o fundo da página.
    <div className="popup-overlay">
      {/* O conteúdo do popup. */}
      <div className="popup-content">
        {/* Botão para fechar o popup. */}
        <span className="close-btn" onClick={onClose}>
          &times;
        </span>
        <h2>Adicionar nova matéria</h2>
        {/* Campo de entrada para o nome da matéria. */}
        <input
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className="popup-input"
          placeholder="Digite o nome da matéria"
        />
        {/* Botões de ação do popup. */}
        <div className="popup-actions">
          <button className="btn-cancel" onClick={onClose}>
            Cancelar
          </button>
          <button className="btn-confirm" onClick={handleConfirm}>
            Confirmar
          </button>
        </div>
      </div>
    </div>
  );
}

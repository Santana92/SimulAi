// Importa o hook useState do React para gerenciar o estado do formulário.
import { useState } from "react";

// Componente para o popup de adição de um novo simulado.
export default function PopupSimulado({ onClose, onConfirm }) {
  // Estado para armazenar o nome do simulado.
  const [nome, setNome] = useState("");
  // Estado para armazenar o arquivo do simulado que foi carregado.
  const [arquivo, setArquivo] = useState(null);

  // Função chamada ao clicar no botão de confirmação.
  const handleConfirm = () => {
    // Validação para garantir que tanto o nome quanto o arquivo foram preenchidos.
    if (!nome.trim() || !arquivo) {
      alert("Por favor, preencha o nome e selecione um arquivo.");
      return;
    }
    // Chama a função onConfirm (passada via props) com o nome e o arquivo.
    onConfirm(nome, arquivo);
    // Limpa os campos do formulário.
    setNome("");
    setArquivo(null);
    // Fecha o popup.
    onClose();
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
        <h2>Adicionar novo simulado</h2>
        {/* Campo de entrada para o nome do simulado. */}
        <input
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className="popup-input"
          placeholder="Digite o nome do simulado"
        />

        {/* Seção para o upload do arquivo. */}
        <label className="popup-label">Carregar arquivo:</label>
        <input
          type="file"
          onChange={(e) => setArquivo(e.target.files[0])}
          className="popup-input-file"
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

// Importa a imagem do logo da aplicação.
import SimulAILogo from "../../assets/SimulAI.png";
// Importa a imagem do avatar do usuário.
import Avatar from "../../assets/Avatar.png";

// Componente funcional para o cabeçalho da aplicação.
export default function Header() {
  return (
    // A tag <header> é usada para o cabeçalho da página, com a classe CSS "header".
    <header className="header">
      {/* Div para o logo da aplicação. */}
      <div className="logo">
        <img src={SimulAILogo} alt="Logo SimulAÍ" />
      </div>
      {/* Div para o menu do usuário, que neste caso contém apenas o avatar. */}
      <div className="user-menu">
        <img src={Avatar} alt="avatar" className="avatar user" />
      </div>
    </header>
  );
}

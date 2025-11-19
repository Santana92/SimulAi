// Importa os componentes necessários do 'react-router-dom' para configurar o roteamento da aplicação.
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Importa os componentes das páginas que serão renderizadas pelas rotas.
import Login from "./components/auth/Login";
import DashboardAluno from "./components/aluno/DashboardAluno";
import DashboardProfessor from "./components/professor/DashboardProfessor";
import Simulado from "./components/simulado/Simulado";
import FeedbackPage from "./components/feedback/FeedbackPage";
// Importa o componente de proteção de rota que acabamos de criar.
import ProtectedRoute from "./components/auth/ProtectedRoute";

// Componente principal da aplicação, agora com rotas protegidas.
function App() {
  return (
    <Router>
      <Routes>
        {/* Rota de Login: pública */}
        <Route path="/" element={<Login />} />

        {/* Rota do Aluno: Protegida. Só permite acesso se o 'userType' no localStorage for 'aluno'. */}
        <Route
          path="/aluno"
          element={
            <ProtectedRoute tipoRequerido="aluno">
              <DashboardAluno />
            </ProtectedRoute>
          }
        />

        {/* Rota do Professor: Protegida. Só permite acesso se o 'userType' no localStorage for 'professor'. */}
        <Route
          path="/professor"
          element={
            <ProtectedRoute tipoRequerido="professor">
              <DashboardProfessor />
            </ProtectedRoute>
          }
        />

        {/* Rota do Simulado: Protegida. Permite acesso a qualquer usuário logado (aluno ou professor). */}
        <Route
          path="/simulado/:simuladoId"
          element={
            <ProtectedRoute requiresAuth={true}>
              <Simulado />
            </ProtectedRoute>
          }
        />

        {/* Rota de Feedback: Protegida. Permite acesso a qualquer usuário logado (aluno ou professor). */}
        <Route
          path="/feedback/:simuladoId"
          element={
            <ProtectedRoute requiresAuth={true}>
              <FeedbackPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

// Exporta o componente App para ser utilizado em outras partes da aplicação (como no main.jsx).
export default App;
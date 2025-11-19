// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';

/**
 * Componente de Rota Protegida.
 *
 * Este componente serve como um "porteiro" para outras rotas da aplicação.
 * Ele verifica se o usuário está logado e/ou se o tipo de usuário
 * corresponde ao tipo exigido pela rota.
 *
 * @param {object} props As propriedades do componente.
 * @param {React.ReactNode} props.children O componente filho (a página) que deve ser renderizado se o usuário for autorizado.
 * @param {string} [props.tipoRequerido] O tipo de usuário ('aluno' ou 'professor') necessário para acessar esta rota.
 * @param {boolean} [props.requiresAuth=false] Se true, a rota exige que qualquer usuário esteja logado, independentemente do tipo.
 * @returns {React.ReactElement} O componente filho se o usuário for autorizado, ou um redirecionamento para a página de login caso contrário.
 */
const ProtectedRoute = ({ children, tipoRequerido, requiresAuth = false }) => {
  // Pega o tipo de usuário que foi salvo no localStorage durante o login.
  const userType = localStorage.getItem('userType');

  // Se a rota exige autenticação (qualquer tipo) e não há usuário logado, redireciona.
  if (requiresAuth && !userType) {
    return <Navigate to="/" replace />;
  }

  // Se um tipo específico é requerido E o usuário logado não corresponde a esse tipo, redireciona.
  // Esta condição só é verificada se tipoRequerido for fornecido.
  if (tipoRequerido && userType !== tipoRequerido) {
    return <Navigate to="/" replace />;
  }

  // Se todas as verificações passarem, permite o acesso e renderiza a página solicitada.
  return children;
};

export default ProtectedRoute;

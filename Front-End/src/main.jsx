// Importa a biblioteca principal do React.
import React from "react";
// Importa o ReactDOM, que fornece métodos específicos do DOM para o React.
import ReactDOM from "react-dom/client";
// Importa o componente principal da aplicação, o 'App'.
import App from "./App";
// Importa a folha de estilos global da aplicação.
import "./index.css";
// Importa o OAuth para o login com o Google
import { GoogleOAuthProvider } from '@react-oauth/google'; 

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* Envolva o App com o Provider */}
    <GoogleOAuthProvider clientId="606985239969-jgaktubf704pbtkot8q112fd8je48naf.apps.googleusercontent.com">
      <App />
    </GoogleOAuthProvider>
  </React.StrictMode>
);
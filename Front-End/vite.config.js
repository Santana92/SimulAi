// Importa a função 'defineConfig' do Vite, que ajuda a ter intellisense e autocompletar para a configuração.
import { defineConfig } from 'vite';

// Importa o plugin oficial do Vite para React, que permite que o Vite entenda e compile arquivos JSX.
import react from '@vitejs/plugin-react';

// URL de referência para a documentação de configuração do Vite.
// https://vitejs.dev/config/

// Exporta a configuração do projeto Vite.
export default defineConfig({
  // A seção 'plugins' é onde configuramos as extensões que o Vite usará.
  plugins: [
    // Adiciona o plugin do React, essencial para compilar a sintaxe do React (JSX) e habilitar funcionalidades como Fast Refresh.
    react()
  ],
});
# Agente SDR Automatizado com IA

Este projeto foi desenvolvido como parte de um processo seletivo e consiste em um assistente de IA totalmente funcional, projetado para automatizar o trabalho de um Sales Development Representative (SDR). A aplicação utiliza a API de Assistants da OpenAI para conduzir conversas naturais, qualificar leads, registrar informações em um funil de vendas no Pipefy e facilitar o agendamento de reuniões através do Calendly.

## Visão Geral do Projeto

O objetivo principal era construir um sistema coeso onde a inteligência artificial não apenas conversasse com o usuário, mas também executasse ações práticas em sistemas externos. O fluxo começa com a interação do usuário através de um webchat. O assistente de IA, então, assume a conversa para coletar informações essenciais como nome, e-mail, empresa e a necessidade do cliente.

Uma vez que os dados são coletados, a IA aciona integrações de backend para persistir essas informações. Caso o cliente demonstre interesse em prosseguir, o assistente consulta a agenda em tempo real e oferece os próximos horários disponíveis. Ao final do processo, é gerado um link de agendamento de uso único, permitindo que o usuário confirme os detalhes e finalize o agendamento em um ambiente seguro e familiar.

## Funcionalidades Principais

  * **Orquestração por IA:** O núcleo da aplicação é gerenciado pela API de Assistants da OpenAI, que controla o fluxo da conversa e decide qual ferramenta (registrar lead, buscar horários) deve ser acionada a cada momento.
  * **Integração com Pipefy:** Todos os leads qualificados são automaticamente registrados em um funil de "Pré-vendas" no Pipefy. Foi implementado um processo de dois passos para garantir a robustez da integração: primeiro, um card é criado com o título do lead; em seguida, ele é atualizado com todos os campos detalhados.
  * **Agendamento via Calendly:** Quando um lead é qualificado, o assistente se conecta à API do Calendly para buscar horários de reunião reais e disponíveis. Após o usuário escolher um horário, o sistema gera um link de agendamento exclusivo, dando ao usuário o controle final para confirmar o evento.
  * **Interface Reativa:** O frontend foi construído com Vue.js, proporcionando uma experiência de chat fluida. A conversa é persistida no navegador usando `localStorage`, permitindo que o usuário continue o diálogo mesmo que a página seja recarregada.

## Tecnologias Utilizadas

  * **Backend:** Python 3, FastAPI, OpenAI API, Pipefy API (GraphQL), Calendly API (REST).
  * **Frontend:** Vue.js 3 (Composition API), Vite, Axios, CSS3.

## Links da Aplicação

  * **Frontend (Live):** [https://desafio-elite-dev-ia-dun.vercel.app/](https://desafio-elite-dev-ia-dun.vercel.app/)
  * **Backend (Live):** [https://desafio-elite-dev-ia.onrender.com](https://desafio-elite-dev-ia.onrender.com)

## Como Executar Localmente

Siga os passos abaixo para configurar и rodar o projeto no seu ambiente de desenvolvimento.

### Pré-requisitos

  * Node.js (versão 20.x ou superior)
  * Python (versão 3.10 ou superior)

### Configuração do Backend

1.  **Navegue até a pasta do backend:**

    ```bash
    cd backend
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Criar
    python3 -m venv venv
    # Ativar (Linux/macOS)
    source venv/bin/activate
    # Ativar (Windows)
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

      * Crie um arquivo chamado `.env` dentro da pasta `backend`.
      * Copie o conteúdo do exemplo abaixo e preencha com suas próprias chaves e IDs.

    <!-- end list -->

    ```env
    # Exemplo de .env
    OPENAI_API_KEY="sk-..."
    PIPEFY_API_KEY="..."
    PIPEFY_PIPE_ID="..."
    CALENDLY_API_KEY="..."
    CALENDLY_USER_URI="https://api.calendly.com/users/..."
    CALENDLY_EVENT_TYPE_URI="https://api.calendly.com/event_types/..."
    ```

5.  **Inicie o servidor:**

    ```bash
    uvicorn main:app --reload
    ```

    O servidor estará disponível em `http://localhost:8000`.

### Configuração do Frontend

1.  **Navegue até a pasta do frontend (em um novo terminal):**

    ```bash
    cd vue-project
    ```

2.  **Instale as dependências:**

    ```bash
    npm install
    ```

3.  **Inicie o servidor de desenvolvimento:**

    ```bash
    npm run dev
    ```

    A aplicação estará disponível em `http://localhost:5173` (ou em outra porta indicada no terminal).

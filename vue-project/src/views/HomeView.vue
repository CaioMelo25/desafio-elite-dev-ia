<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';

const messages = ref([]);
const newMessage = ref('');
const threadId = ref(null); 
const isLoading = ref(false); 


onMounted(() => {
  const savedThreadId = localStorage.getItem('chat_thread_id');
  if (savedThreadId) {
    threadId.value = savedThreadId;
    messages.value.push({ id: Date.now(), sender: 'bot', text: 'Olá! Retomando nossa conversa.' });
  } else {
    messages.value.push({ id: Date.now(), sender: 'bot', text: 'Olá! Como posso ajudar você hoje?' });
  }
});

const scrollToBottom = async () => {
  await nextTick();
  const messagesArea = document.querySelector('.messages-area');
  if (messagesArea) {
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }
};

const sendMessage = async () => {
  const userMessage = newMessage.value.trim();
  if (userMessage === '') return;

  messages.value.push({ id: Date.now(), sender: 'user', text: userMessage });
  newMessage.value = '';
  await scrollToBottom();

  isLoading.value = true;

  try {
    const response = await axios.post('https://desafio-elite-dev-ia.onrender.com/chat', {
      message: userMessage,
      thread_id: threadId.value
    });

    const botResponse = response.data;

    messages.value.push({ id: Date.now() + 1, sender: 'bot', text: botResponse.response });
    
    threadId.value = botResponse.thread_id;
    localStorage.setItem('chat_thread_id', threadId.value);

  } catch (error) {
    console.error("Erro ao conectar com o backend:", error);
    messages.value.push({ id: Date.now() + 1, sender: 'bot', text: 'Desculpe, estou com problemas para me conectar ao servidor. Por favor, tente novamente mais tarde.' });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};
</script>

<template>
  <main class="chat-container">
    <div class="messages-area">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="message.sender === 'bot' ? 'bot' : 'user'"
      >
        <p v-for="(line, index) in message.text.split('\n')" :key="index">{{ line }}</p>
      </div>
      <div v-if="isLoading" class="message bot typing-indicator">
        <span></span><span></span><span></span>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="message-form">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Digite sua mensagem..."
        class="message-input"
        :disabled="isLoading"
      />
      <button type="submit" class="send-button" :disabled="isLoading">Enviar</button>
    </form>
  </main>
</template>

<style scoped>
/* Os estilos foram aprimorados, incluindo o indicador de "digitando" */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 90vh;
  max-width: 700px;
  margin: 2rem auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.messages-area {
  flex-grow: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.message {
  padding: 0.75rem 1.25rem;
  border-radius: 18px;
  max-width: 80%;
  line-height: 1.4;
}
.message p {
  margin: 0;
}
.bot {
  background-color: #e5e7eb;
  color: #1f2937;
  align-self: flex-start;
}
.user {
  background-color: #3b82f6;
  color: white;
  align-self: flex-end;
}
.message-form {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background-color: #ffffff;
}
.message-input {
  flex-grow: 1;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 1rem;
}
.message-input:disabled {
  background-color: #f3f4f6;
}
.send-button {
  margin-left: 1rem;
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: #3b82f6;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
}
.send-button:hover { background-color: #2563eb; }
.send-button:disabled { background-color: #9ca3af; cursor: not-allowed; }

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #9ca3af;
  border-radius: 50%;
  display: inline-block;
  margin: 0 1px;
  animation: bounce 1.4s infinite ease-in-out both;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>
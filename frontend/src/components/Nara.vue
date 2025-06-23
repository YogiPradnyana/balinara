<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch, computed, h } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import Nara from './icons/Nara.vue'
import ChatBuble from './icons/ChatBuble.vue'
import FilledSend from './icons/FilledSend.vue'
import {
  showNotification,
  showConfirmationToast,
  dismissCurrentConfirmationToast,
} from '@/services/notificationService'
import ConfirmationToast from '@/components/ConfirmationToast.vue'

const chatStore = useChatStore()

const userInput = ref('')
const isOpen = ref(false)
const messagesContainer = ref(null)
const userInputField = ref(null)

const showCalloutMessage = ref(false)
const calloutTexts = ['How can I help?', 'Ask me anything!', 'Hello Traveler!👋']
const currentCalloutText = ref('')
const calloutInterval = ref(null)
const calloutDisplayTimeout = ref(null)

// Menggunakan computed properties untuk mengakses state dari store
const messages = computed(() => chatStore.messages)
const isSending = computed(() => chatStore.isSendingMessage)
const isLoadingHistory = computed(() => chatStore.isLoadingHistory)
const error = computed(() => chatStore.error)

const handleSendMessage = async () => {
  if (!userInput.value.trim()) return

  const messageText = userInput.value
  userInput.value = '' // Kosongkan input segera

  await nextTick()
  if (userInputField.value) {
    userInputField.value.style.height = 'auto'
  }

  // Cukup panggil action store. Store yang akan menangani semuanya.
  try {
    await chatStore.sendMessage(messageText)
    focusUserInput()
    // focusUserInput()
  } catch (err) {
    // Error sudah ditangani di store, di sini hanya untuk log jika perlu
    console.error('Component caught an error from sendMessage action:', err)
  }
}

const sendSuggestedReply = (reply) => {
  chatStore.sendMessage(reply) // Langsung panggil action store
}

const handleClearHistory = () => {
  // Gunakan toast konfirmasi canggih Anda
  const onConfirm = () => {
    chatStore.clearSession()
    showNotification('success', 'Chat session has been reset.')
    dismissCurrentConfirmationToast()
    focusUserInput()
  }

  showConfirmationToast(
    h(ConfirmationToast, {
      message: 'Are you sure you want to clear this chat session?',
      onConfirm,
      onCancel: dismissCurrentConfirmationToast,
    }),
  )
}

// Fungsi untuk memformat pesan (misal: markdown sederhana)
const formatMessage = (text) => {
  if (!text) return ''
  let formattedText = text.replace(/\n/g, '<br>')
  formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
  formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
  return formattedText
}

const displayNextCallout = () => {
  if (isOpen.value) {
    showCalloutMessage.value = false
    return
  }
  const randomIndex = Math.floor(Math.random() * calloutTexts.length)
  currentCalloutText.value = calloutTexts[randomIndex]
  showCalloutMessage.value = true
  if (calloutDisplayTimeout.value) clearTimeout(calloutDisplayTimeout.value)
  calloutDisplayTimeout.value = setTimeout(() => {
    showCalloutMessage.value = false
  }, 4000)
}

const focusUserInput = () => {
  if (userInputField.value) {
    userInputField.value.focus()
  } else {
    console.log('userInputField is null, cannot focus.')
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const suggestedReplies = ref([
  'Tourist attractions in Bali',
  'Recommended interesting places',
  'Cultural experiences',
  'Adventure activities',
])

onMounted(() => {
  chatStore.startSession()

  // Panggil fetchHistory jika ada session dan pesan masih kosong
  if (chatStore.sessionId && chatStore.messages.length === 0) {
    chatStore.fetchHistory()
  }

  setTimeout(() => {
    displayNextCallout()
    calloutInterval.value = setInterval(displayNextCallout, 10000)
  }, 2000)
})

onUnmounted(() => {
  if (calloutInterval.value) clearInterval(calloutInterval.value)
  if (calloutDisplayTimeout.value) clearTimeout(calloutDisplayTimeout.value)
})

watch(
  messages,
  () => {
    scrollToBottom()
  },
  { deep: true },
)

// Watcher untuk auto-focus (sudah bagus)
watch(
  isOpen,
  (newValue) => {
    if (calloutInterval.value) clearInterval(calloutInterval.value)
    if (calloutDisplayTimeout.value) clearTimeout(calloutDisplayTimeout.value)
    if (newValue) {
      showCalloutMessage.value = false
      // nextTick() di sini juga baik untuk memastikan elemen ada
      nextTick(() => {
        scrollToBottom()
        focusUserInput()
      })
    } else {
      setTimeout(() => {
        displayNextCallout()
        calloutInterval.value = setInterval(displayNextCallout, 10000)
      }, 1000)
    }
  },
  { flush: 'post' },
)

const autoResizeTextarea = () => {
  if (userInputField.value) {
    userInputField.value.style.height = 'auto' // Reset tinggi untuk perhitungan yang benar
    userInputField.value.style.height = `${userInputField.value.scrollHeight}px`
  }
}
</script>

<style scoped>
/* Pastikan Anda sudah mengimpor atau mendefinisikan warna dari Tailwind CSS Anda
   seperti pr-500, neu-900, sur-50, dll. Ini penting agar styling bekerja. */

.callout-fade-enter-active,
.callout-fade-leave-active {
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}
.callout-fade-enter-from,
.callout-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Custom scrollbar for Webkit browsers (Chrome, Safari) */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Untuk Firefox (jika diperlukan) */
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

/* Loading/Error state styles */
.loading-indicator,
.error-message-chat {
  text-align: center;
  padding: 10px;
  font-size: 0.85em;
  color: #555;
}
.loading-indicator {
  color: #007bff;
}
.error-message-chat {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  margin: 10px;
}
</style>

<template>
  <div class="fixed bottom-5 right-5 z-50 font-pr text-neu-900">
    <Transition name="callout-fade">
      <div
        v-if="showCalloutMessage && !isOpen"
        class="absolute bottom-full right-0 mb-4 min-w-[150px] max-w-[200px] p-3 bg-white rounded-xl shadow-lg text-sm z-10"
      >
        <div
          class="absolute bottom-[-8px] right-[20px] w-0 h-0 border-l-[8px] border-l-transparent border-t-[8px] border-t-white border-r-[8px] border-r-transparent"
        ></div>
        {{ currentCalloutText }}
      </div>
    </Transition>
    <button
      @click="toggleChat"
      class="text-white cursor-pointer rounded-full flex items-center justify-center transition-transform duration-300 ease-in-out"
      :class="[isOpen ? 'shadow-lg rotate-90 hidden sm:block bg-pr-500 p-3' : 'hover:scale-105']"
      aria-label="Toggle Chat"
      :aria-expanded="isOpen.toString()"
    >
      <svg
        v-if="isOpen"
        xmlns="http://www.w3.org/2000/svg"
        class="h-8 w-8"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
      <Nara class="w-14" v-else />
    </button>

    <transition
      enter-active-class="transition ease-out duration-300 transform"
      enter-from-class="opacity-0 translate-y-10 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition ease-in duration-200 transform"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-10 scale-95"
    >
      <div
        v-if="isOpen"
        class="fixed bottom-0 right-0 sm:bottom-24 sm:right-5 w-full sm:w-[380px] h-full sm:h-[calc(100vh-120px)] sm:max-h-[600px] sm:rounded-3xl shadow-xl flex flex-col overflow-hidden"
        role="log"
        aria-live="polite"
      >
        <div class="bg-pr-500 text-white flex flex-col gap-2 items-center p-3">
          <button
            @click="toggleChat"
            class="absolute top-3 block sm:hidden right-3 text-white p-1.5 rounded-md hover:bg-white/20 transition-colors"
            aria-label="Close Chat"
          >
            <svg
              v-if="isOpen"
              xmlns="http://www.w3.org/2000/svg"
              class="size-4.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div
            class="bg-pr-700 px-4 py-1.5 rounded-full text-sm font-semibold flex items-center gap-1.5"
          >
            <ChatBuble class="w-4.5" />
            <span>Conversations</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="flex items-center justify-center px-[5px] py-1.5 bg-white rounded-full">
              <Nara class="w-7.5" />
            </div>
            <h2 class="font-semibold">Nara</h2>
          </div>
        </div>

        <div
          ref="messagesContainer"
          class="flex-grow px-3 pt-6 space-y-3 overflow-y-auto bg-[#FAFAFA] scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100"
          aria-atomic="false"
          aria-relevant="additions"
          style="overscroll-behavior-y: contain"
        >
          <div v-if="isLoadingHistory" class="loading-indicator">Loading chat history...</div>
          <div
            v-if="error && !isLoadingHistory && messages.length === 0"
            class="error-message-chat"
          >
            {{ error }}
          </div>
          <div
            v-if="messages.length === 0 && !error && !isLoadingHistory"
            class="loading-indicator"
          >
            Start your conversation with Nara! Ask anything about Bali.
          </div>

          <div v-for="message in messages" :key="message.id">
            <div class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
              <div
                class="max-w-[90%] p-3 rounded-2xl text-sm"
                :class="{
                  'bg-pr-500 text-neu-50 font-light rounded-tl-none': message.sender !== 'user', // JIKA BUKAN 'user', ANGGAP BOT
                  'bg-neu-100 rounded-tr-none': message.sender === 'user',
                }"
              >
                <p v-html="formatMessage(message.text)"></p>
                <small
                  v-if="message.timestamp"
                  class="block text-right mt-1 text-[10px]"
                  :class="message.sender === 'user' ? 'text-neu-500' : 'text-white/70'"
                >
                  {{
                    new Date(message.timestamp).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })
                  }}
                </small>
              </div>
            </div>
          </div>
          <!-- Indikator Bot Sedang Mengetik/Memproses -->
          <div
            v-if="isSending && messages[messages.length - 1]?.sender === 'user'"
            class="flex justify-start"
          >
            <div
              class="max-w-[70%] p-2.5 rounded-xl shadow-sm bg-white dark:bg-gray-600 border border-gray-200 dark:border-gray-500 rounded-bl-none"
            >
              <div class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
                <div
                  class="animate-pulse w-1.5 h-1.5 bg-gray-400 dark:bg-gray-500 rounded-full"
                ></div>
                <div
                  class="animate-pulse delay-100 w-1.5 h-1.5 bg-gray-400 dark:bg-gray-500 rounded-full"
                ></div>
                <div
                  class="animate-pulse delay-200 w-1.5 h-1.5 bg-gray-400 dark:bg-gray-500 rounded-full"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col bg-sur-50 gap-3 px-3 pt-3 pb-4 drop-shadow-[0px_-4px_32px_#2121210F]"
        >
          <div
            v-if="suggestedReplies.length > 0 && !isSending && !isLoadingHistory"
            class="flex space-x-2 overflow-x-auto pb-1 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent"
          >
            <button
              v-for="reply in suggestedReplies"
              :key="reply"
              @click="sendSuggestedReply(reply)"
              class="whitespace-nowrap cursor-pointer px-3 py-1 border border-pr-500 text-pr-500 hover:bg-pr-50 rounded-full text-sm font-medium transition-colors"
            >
              {{ reply }}
            </button>
          </div>

          <form @submit.prevent="handleSendMessage" class="flex items-center space-x-2">
            <textarea
              ref="userInputField"
              v-model="userInput"
              @input="autoResizeTextarea"
              @keydown.enter.exact.prevent="handleSendMessage"
              placeholder="Start a conversation..."
              class="flex-grow p-2.5 rounded-lg focus:ring-1 focus:ring-neu-200 focus:border-transparent outline-none text-sm resize-none overflow-hidden"
              rows="1"
              :disabled="isSending || isLoadingHistory"
              aria-label="Chat input"
            ></textarea>

            <button
              type="submit"
              class="bg-pr-500 hover:bg-pr-600 cursor-pointer flex items-center justify-center text-white size-10 rounded-lg"
              aria-label="Send Message"
              :disabled="isSending || !userInput.trim() || isLoadingHistory"
            >
              <FilledSend class="size-5" />
            </button>
          </form>
          <button
            @click="handleClearHistory"
            v-if="messages.length > 0"
            class="w-full mt-2.5 py-1.5 text-xs text-center text-gray-500 hover:text-red-600 disabled:text-gray-300 transition-colors"
          >
            Clear Chat History
          </button>
          <div
            v-if="error && !isSending && !isLoadingHistory"
            class="mt-2 text-center text-red-500 text-xs"
          >
            {{ error }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

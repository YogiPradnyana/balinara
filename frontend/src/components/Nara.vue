<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import Nara from './icons/Nara.vue'
import ChatBuble from './icons/ChatBuble.vue'
import FilledSend from './icons/FilledSend.vue'

const isOpen = ref(false) // Awalnya tertutup
const userInput = ref('')
const messagesContainer = ref(null) // Untuk auto-scroll

// State untuk pesan callout
const showCalloutMessage = ref(false)
const calloutTexts = [
  'Ada yang bisa dibantu?',
  'Tanya aku apa saja!',
  'Butuh bantuan navigasi?',
  'Halo Traveler!👋',
]
const currentCalloutText = ref('')
let calloutInterval = null
let calloutDisplayTimeout = null // Timeout untuk menyembunyikan callout setelah beberapa detik

const displayNextCallout = () => {
  if (isOpen.value) {
    // Jangan tampilkan jika chat sudah terbuka
    showCalloutMessage.value = false
    return
  }

  // Pilih teks acak dari array
  const randomIndex = Math.floor(Math.random() * calloutTexts.length)
  currentCalloutText.value = calloutTexts[randomIndex]
  showCalloutMessage.value = true

  // Sembunyikan callout setelah beberapa detik
  clearTimeout(calloutDisplayTimeout) // Hapus timeout sebelumnya jika ada
  calloutDisplayTimeout = setTimeout(() => {
    showCalloutMessage.value = false
  }, 4000) // Tampilkan selama 4 detik
}

onMounted(() => {
  // Tampilkan callout pertama setelah beberapa detik delay awal
  setTimeout(() => {
    displayNextCallout()
    // Atur interval untuk menampilkan callout berikutnya
    // Total waktu: 4 detik tampil + 6 detik tunggu = 10 detik per siklus
    calloutInterval = setInterval(displayNextCallout, 10000) // Munculkan pesan baru setiap 10 detik
  }, 2000) // Delay awal 2 detik sebelum callout pertama muncul
})

onUnmounted(() => {
  clearInterval(calloutInterval)
  clearTimeout(calloutDisplayTimeout)
})

const messages = ref([
  {
    id: 1,
    sender: 'bot',
    text: "Hello Udin! I'm Nara, your virtual guide who will help you with your trip in Bali.",
  },
  { id: 2, sender: 'bot', text: 'How can I help you?' },
  { id: 3, sender: 'user', text: 'I like hiking, help me find a mountain in Bali' },
])

const suggestedReplies = ref([
  'Tourist attractions in Bali',
  'Recommended interesting places',
  'Cultural experiences',
  'Adventure activities',
])

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    // Jika chat dibuka, sembunyikan callout dan hentikan sementara interval
    showCalloutMessage.value = false
    clearTimeout(calloutDisplayTimeout) // Hapus timeout jika ada
    scrollToBottom()
  }
}

const scrollToBottom = async () => {
  await nextTick() // Tunggu DOM update
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = () => {
  if (userInput.value.trim() === '') return

  messages.value.push({
    id: Date.now(),
    sender: 'user',
    text: userInput.value.trim(),
  })
  const currentInput = userInput.value.trim()
  userInput.value = ''
  scrollToBottom()

  // Simulate bot response
  setTimeout(() => {
    let botResponse = "I'm sorry, I'm still learning. Can you try asking something else?"
    if (
      currentInput.toLowerCase().includes('mountain') ||
      currentInput.toLowerCase().includes('hiking')
    ) {
      botResponse =
        'Great! For hiking in Bali, I recommend Mount Batur for sunrise trekking or Mount Agung for a more challenging climb. Would you like more details on either?'
      suggestedReplies.value = [
        'Tell me about Mount Batur',
        'Details on Mount Agung',
        'Any other suggestions?',
      ]
    } else if (currentInput.toLowerCase().includes('tourist attractions')) {
      botResponse =
        'Bali has many famous attractions! For example, Tanah Lot Temple, Uluwatu Temple, or the Tegallalang Rice Terraces. Which one are you interested in?'
      suggestedReplies.value = ['Tanah Lot', 'Uluwatu', 'Tegallalang']
    } else {
      suggestedReplies.value = [
        'Tourist attractions in Bali',
        'Adventure activities',
        'Help with booking',
      ]
    }

    messages.value.push({
      id: Date.now() + 1,
      sender: 'bot',
      text: botResponse,
    })
    scrollToBottom()
  }, 1000)
}

const sendSuggestedReply = (reply) => {
  userInput.value = reply
  sendMessage()
}

// Untuk contoh, kita buka otomatis setelah beberapa saat jika ingin testing UI terbuka
// setTimeout(() => {
//   if (!isOpen.value) {
//     toggleChat()
//   }
// }, 1000)
</script>

<style scoped>
.callout-fade-enter-active,
.callout-fade-leave-active {
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}
.callout-fade-enter-from,
.callout-fade-leave-to {
  opacity: 0;
  transform: translateY(10px); /* Muncul dari sedikit ke bawah dan fade in */
}

/* Custom scrollbar for Webkit browsers (Chrome, Safari) */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px; /* Lebar scrollbar horizontal dan vertikal */
  height: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent; /* Warna track, bisa juga bg-gray-100 dari Tailwind */
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #cbd5e1; /* Warna thumb (bg-gray-300 dari Tailwind) */
  border-radius: 10px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #94a3b8; /* Warna thumb saat hover (bg-gray-400 dari Tailwind) */
}

/* Untuk Firefox (jika diperlukan, Tailwind biasanya sudah cukup baik) */
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent; /* thumb track */
}
</style>

<template>
  <div class="fixed bottom-5 right-5 z-50 font-pr text-neu-900">
    <!-- Pesan Callout/Notifikasi di atas ikon -->
    <Transition name="callout-fade">
      <div
        v-if="showCalloutMessage && !isOpen"
        class="absolute bottom-full right-0 mb-4 min-w-[150px] max-w-[200px] p-3 bg-white rounded-xl shadow-lg text-sm z-10"
      >
        <!-- Segitiga kecil penunjuk ke bawah -->
        <div
          class="absolute bottom-[-8px] right-[20px] w-0 h-0 border-l-[8px] border-l-transparent border-t-[8px] border-t-white border-r-[8px] border-r-transparent"
        ></div>
        {{ currentCalloutText }}
      </div>
    </Transition>
    <!-- Tombol Toggler Chat -->
    <button
      @click="toggleChat"
      class="text-white cursor-pointer rounded-full flex items-center justify-center transition-transform duration-300 ease-in-out"
      :class="[isOpen ? 'shadow-lg rotate-90 hidden sm:block bg-pr-500 p-3' : 'hover:scale-105']"
      aria-label="Toggle Chat"
    >
      <!-- Ikon X jika terbuka, ikon chat jika tertutup -->
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

    <!-- Jendela Chat -->
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
      >
        <!-- Header Chat -->
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

        <!-- Pesan-pesan -->
        <div
          ref="messagesContainer"
          class="flex-grow px-3 pt-6 space-y-3 overflow-y-auto bg-[#FAFAFA] scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100"
        >
          <!-- Timestamp -->
          <div class="text-center text-sm text-neu-500 pb-2">Sun, 27 April 25</div>
          <div v-for="message in messages" :key="message.id">
            <div class="flex" :class="message.sender === 'bot' ? 'justify-start' : 'justify-end'">
              <div
                class="max-w-[90%] p-3 rounded-2xl text-sm"
                :class="{
                  'bg-pr-500 text-neu-50 font-light rounded-tl-none': message.sender === 'bot',
                  'bg-neu-100  rounded-tr-none': message.sender === 'user',
                }"
              >
                <p style="white-space: pre-line">{{ message.text }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div
          class="flex flex-col bg-sur-50 gap-3 px-3 pt-3 pb-4 drop-shadow-[0px_-4px_32px_#2121210F]"
        >
          <!-- Suggested Replies -->
          <div
            v-if="suggestedReplies.length > 0"
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

          <div class="flex items-center space-x-2">
            <input
              type="text"
              v-model="userInput"
              @keyup.enter="sendMessage"
              placeholder="Start a conversation..."
              class="flex-grow p-2.5 rounded-lg text-sm focus:ring-1 focus:ring-neu-200 focus:border-transparent outline-none"
            />
            <button
              @click="sendMessage"
              class="bg-pr-500 hover:bg-pr-600 cursor-pointer flex items-center justify-center text-white size-10 rounded-lg"
              aria-label="Send Message"
            >
              <FilledSend class="size-5" />
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

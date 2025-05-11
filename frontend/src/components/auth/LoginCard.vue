<script setup>
import Exit from '../icons/Exit.vue'
import Mail from '../icons/Mail.vue'
import Google from '../icons/social-media/Google.vue'

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr text-neu-900 bg-neu-900/50 flex items-center justify-center z-50"
  >
    <!-- Card Login -->

    <div
      class="bg-white px-4 pt-4 pb-8 flex-col flex items-end rounded-3xl w-full max-w-md animate-fadeIn"
    >
      <Exit class="size-5 cursor-pointer hover:text-neu-500 transition" @click="handleClose" />
      <div class="w-full mt-4 px-4">
        <h1 class="text-[32px] text-center font-semibold leading-[38px]">
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div class="w-full flex flex-col items-center">
          <h2 class="text-xl font-semibold mt-6 leading-8 text-center w-8/12">
            Sign in to unlock the best of Balinara.
          </h2>
        </div>
        <div class="flex flex-col gap-6 mt-12">
          <button
            type="button"
            class="border-[1.2px] rounded-full cursor-pointer border-neu-900 flex gap-3 px-6 py-3 justify-center items-center font-medium"
          >
            <Google />
            Continue with Google
          </button>
          <button
            type="button"
            class="border-[1.2px] rounded-full cursor-pointer border-neu-900 flex gap-3 px-6 py-3 justify-center items-center font-medium"
          >
            <Mail />
            Continue with Email
          </button>
        </div>
        <div class="w-full flex justify-center mt-12">
          <p class="text-neu-800 text-xs leading-4.5 text-center w-3/4">
            By proceeding, you accept our <span class="text-pr-500">terms of use</span> and
            <span class="text-pr-500">privacy policy</span>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style>

<script setup>
import Exit from '@/components/icons/Exit.vue'

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999"
  >
    <!-- Card Login -->

    <div
      class="bg-white px-4 pt-4 pb-8 flex-col flex items-end rounded-3xl w-full max-w-lg md:max-w-[524px] animate-fadeIn"
    >
      <Exit class="size-5 cursor-pointer hover:text-neu-500 transition" @click="handleClose" />
      <div class="w-full mt-4 px-4">
        <h1
          class="text-[28px] md:text-[32px] text-center font-se font-semibold leading-7 md:leading-[38px]"
        >
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div class="w-full flex flex-col items-center gap-3">
          <h2 class="text-xl md:text-2xl font-semibold mt-5 md:mt-6 leading-8 text-center w-11/12">
            🎉Thanks for Sharing Your Bali Experience!
          </h2>
          <p class="text-neu-600 text-sm md:text-base text-center">
            Your review has been posted and is now helping fellow travelers explore Bali more
            confidently and meaningfully.
          </p>
        </div>
        <div class="flex flex-col sm:flex-row text-sm md:text-base gap-3 mt-12">
          <button
            class="px-4.5 py-3.5 flex flex-1 items-center cursor-pointer text-pr-500 hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium bg-sur-50 rounded-full border border-pr-500"
          >
            Write Another Review
          </button>
          <button
            @click="handleClose"
            class="px-4.5 py-3.5 flex flex-1 gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium bg-pr-500 rounded-full text-neu-50"
          >
            Back
          </button>
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

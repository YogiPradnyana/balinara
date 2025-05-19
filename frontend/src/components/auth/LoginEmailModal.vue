<script setup>
import ArrowLeftBold from '../icons/ArrowLeftBold.vue'
import Exit from '../icons/Exit.vue'
import Show from '../icons/Show.vue'

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-50"
  >
    <div
      class="bg-white px-4 pt-4 pb-8 flex-col flex items-end rounded-3xl w-full max-w-sm md:max-w-lg animate-fadeIn"
    >
      <div class="flex justify-between items-center w-full">
        <ArrowLeftBold
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose"
        />
        <Exit class="size-5 cursor-pointer hover:text-neu-500 transition" @click="handleClose" />
      </div>
      <div class="w-full flex flex-col items-center mt-4 px-4">
        <h1
          class="text-[28px] md:text-[32px] text-center font-semibold leading-7 md:leading-[38px]"
        >
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div
          class="flex gap-2 sm:gap-2.5 mt-5 md:mt-6 p-1 items-center w-fit rounded-full bg-sur-100"
        >
          <button
            type="button"
            class="px-8 sm:px-10 md:px-12 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Sign in
          </button>
          <button
            type="button"
            class="px-8 sm:px-10 md:px-12 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-none rounded-full text-neu-500"
          >
            Sign up
          </button>
        </div>
        <h2 class="text-lg sm:text-xl font-semibold mt-4 md:mt-6 leading-8 w-full">
          Welcome back.
        </h2>
        <form class="flex flex-col w-full">
          <div class="space-y-4 mt-5 md:mt-8 w-full">
            <div class="flex flex-col gap-3">
              <label class="text-sm font-semibold">Email</label>
              <input
                type="email"
                class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                placeholder="Email"
              />
            </div>
            <div class="flex flex-col gap-3">
              <label class="text-sm font-semibold">Password</label>
              <div class="relative flex">
                <input
                  type="password"
                  class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
                  placeholder="Password"
                />
                <Show class="size-5.5 absolute top-1/2 -translate-y-1/2 right-3" />
              </div>
            </div>
            <p class="text-sm md:text-base font-medium underline">Forgot password?</p>
          </div>
          <button
            type="submit"
            class="px-4.5 w-full py-2.5 md:py-3 flex gap-2 mt-8 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Sign in
          </button>
        </form>
        <div class="w-full flex justify-center mt-5 md:mt-8">
          <p class="text-neu-800 text-xs leading-4.5 text-center w-3/4">
            By proceeding, you accept our
            <span class="text-pr-500">terms of use</span> and
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

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import Exit from './icons/Exit.vue'
import ArrowLeftBold from './icons/ArrowLeftBold.vue'
import StarFilled from './icons/StarFilled.vue'
import Heart from './icons/Heart.vue'
import DoubleQuotes from './icons/DoubleQuotes.vue'
import ArrowLeft from './icons/ArrowLeft.vue'
import ArrowRight from './icons/ArrowRight.vue'

const authStore = useAuthStore()

const emit = defineEmits(['close'])

const handleClose = () => {
  isLoginEmailOpen.value = false
  isRegisterEmailOpen.value = false
  emit('close')
}

const isLoginEmailOpen = ref(false)
const isRegisterEmailOpen = ref(false)

watch(
  () => authStore.isAuthenticated,
  (isAuth) => {
    if (isAuth) {
      console.log(isAuth)

      handleClose()
    }
  },
)
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999"
  >
    <!-- Image Review Modal -->

    <div
      class="bg-white px-6 pb-6 flex-col flex items-end rounded-3xl w-[95%] lg:w-[90%] h-[95%] overflow-y-auto lg:h-fit animate-fadeIn"
    >
      <div
        class="flex justify-between items-center bg-white w-full py-6 sticky top-0 lg:static z-10"
      >
        <div
          class="flex items-center gap-1 text-sm md:text-base font-medium hover:underline transition cursor-pointer"
        >
          <ArrowLeftBold class="size-5" @click="handleClose(false)" aria-label="Back" />Back to
          album
        </div>
        <Exit
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(true)"
          aria-label="Close"
        />
      </div>
      <div class="w-full mt-2 flex-1 flex flex-col">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2 md:gap-3">
            <h1
              class="text-[28px] md:text-[32px] font-semibold leading-7 md:leading-[38px] font-se"
            >
              Tanah Lot
            </h1>
            <div class="bg-neu-100 w-[1.2px] h-7"></div>
            <div class="flex gap-0.5 items-center text-sm md:text-base">
              <StarFilled class="size-5" />
              4.5 (532 reviews)
            </div>
          </div>
          <div
            class="px-2 sm:px-4 border-neu-200 text-sm sm:text-base border-[1.6px] gap-2 py-2 rounded-full font-medium items-center flex"
          >
            <Heart class="size-5 sm:size-6 cursor-pointer" />
            <span class="hidden sm:block">Save</span>
          </div>
        </div>
        <div class="w-full h-[1.6px] bg-neu-100"></div>
        <div class="flex-1 flex-col lg:flex-row flex mt-4 gap-10 lg:gap-4">
          <div class="lg:max-w-sm w-full">
            <div class="gap-2 mt-3 min-w-fit flex items-center">
              <img
                src="@/assets/images/User Avatar.jpg"
                alt="User Profile"
                class="size-10 rounded-full"
              />
              <div class="space-y-0.5">
                <h3 class="font-medium whitespace-nowrap text-sm">Udin Surudin</h3>
                <p class="text-xs text-neu-600">10 Contributions</p>
              </div>
            </div>
            <div class="flex mt-2 gap-0.5 items-center">
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
            </div>
            <div class="flex-col flex gap-2 mt-4">
              <DoubleQuotes class="size-6 sm:size-8 text-neu-900" />
              <p class="text-neu-600 text-sm sm:text-base">
                Must visit place, but too crowded. The temple you see you are not allowed to go in
                anyway. Rock formations out at sea, Tanah Lot is quite a tourist attraction, about
                40mins north of Seminyak. Best times to visit are around sunrise or sunset.
              </p>
            </div>
            <p class="text-sm font-medium mt-4">January 2025</p>
          </div>
          <div
            class="lg:flex-1 shrink-0 h-[420px] lg:h-[480px] overflow-hidden rounded-2xl relative"
          >
            <div
              class="absolute top-1/2 -translate-y-1/2 z-50 flex justify-between items-center w-full px-5"
            >
              <div
                class="ps-1 pe-1.5 py-[5px] cursor-pointer flex items-center w-fit h-fit justify-center bg-neu-900 transition-colors hover:bg-neu-800 rounded-full"
              >
                <ArrowLeft class="size-6 sm:size-7 xl:size-9 text-neu-50" />
              </div>
              <div
                class="ps-1.5 pe-1 py-[5px] cursor-pointer flex items-center w-fit h-fit justify-center bg-neu-900 transition-colors hover:bg-sur-50/10 rounded-full"
              >
                <ArrowRight class="size-6 sm:size-7 xl:size-9 text-neu-50" />
              </div>
            </div>
            <div class="relative h-full w-full bg-neu-900">
              <img
                src="@/assets/images/tanah-lot.webp"
                class="w-full h-full object-contain"
                alt=""
              />
              <div
                class="absolute left-1/2 whitespace-nowrap top-4 -translate-x-1/2 transform rounded-full bg-neu-900 bg-opacity-60 px-5 py-1 text-sm text-white"
              >
                11 of 5000 in All Photos
              </div>
            </div>
          </div>
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

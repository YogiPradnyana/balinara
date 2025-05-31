<script setup>
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999999"
  >
    <div class="bg-white px-4 pt-4 pb-8 flex-col flex rounded-3xl w-full max-w-150 animate-fadeIn">
      <div class="flex justify-end w-full">
        <Exit
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(true)"
        />
      </div>
      <form class="w-full flex flex-col mt-4 space-y-6 px-4">
        <div class="flex flex-col gap-1">
          <h1 class="text-3xl font-se font-semibold">Edit Facility</h1>
          <div class="flex gap-2 items-center text-sm font-medium">
            <span>Katalog</span>
            <ArrowRight class="size-4 text-neu-500" />
            <div @click="handleClose" class="hover:underline">Facilities</div>
            <ArrowRight class="size-4 text-neu-500" />
            <span class="text-neu-500">Edit</span>
          </div>
        </div>
        <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col flex-1 gap-4">
          <div class="flex flex-col gap-3">
            <label for="name" class="text-base font-semibold">Facility Name</label>
            <input
              type="text"
              id="name"
              placeholder="Name"
              value="Parking"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
          <div class="flex flex-col gap-3">
            <label for="descriptions" class="text-base font-semibold">SVG</label>
            <textarea
              id="descriptions"
              rows="7"
              placeholder="SVG Tag"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
            >
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M12.0004 21.9329C10.0358 21.9329 8.11538 21.3503 6.48191 20.2589C4.84843 19.1674 3.5753 17.6161 2.82349 15.8011C2.07169 13.9861 1.87498 11.9889 2.25825 10.0621C2.64151 8.13525 3.58754 6.36536 4.9767 4.97621C6.36585 3.58705 8.13574 2.64103 10.0626 2.25776C11.9894 1.87449 13.9866 2.0712 15.8016 2.823C17.6166 3.57481 19.1679 4.84795 20.2594 6.48142C21.3508 8.11489 21.9334 10.0353 21.9334 11.9999C21.9305 14.6334 20.883 17.1582 19.0209 19.0204C17.1587 20.8825 14.6339 21.93 12.0004 21.9329ZM12.0004 3.0669C10.2336 3.0669 8.5065 3.59081 7.03748 4.57238C5.56845 5.55395 4.42349 6.9491 3.74737 8.58139C3.07125 10.2137 2.89435 12.0098 3.23903 13.7426C3.58371 15.4755 4.4345 17.0672 5.6838 18.3165C6.9331 19.5658 8.52481 20.4166 10.2576 20.7613C11.9905 21.1059 13.7866 20.929 15.4189 20.2529C17.0512 19.5768 18.4463 18.4318 19.4279 16.9628C20.4095 15.4938 20.9334 13.7667 20.9334 11.9999C20.9307 9.63153 19.9887 7.36093 18.314 5.68624C16.6394 4.01155 14.3688 3.06955 12.0004 3.0669Z"
      fill="currentColor"
      stroke="currentColor"
      stroke-width="0.6"
    />
    <path
      d="M12.5693 8H10.4693C10.3511 7.99984 10.234 8.02301 10.1247 8.06819C10.0155 8.11336 9.91619 8.17965 9.83259 8.26325C9.74898 8.34686 9.6827 8.44613 9.63752 8.5554C9.59235 8.66466 9.56918 8.78177 9.56934 8.9V15.788C9.56934 15.9471 9.63255 16.0997 9.74507 16.2123C9.85759 16.3248 10.0102 16.388 10.1693 16.388C10.3285 16.388 10.4811 16.3248 10.5936 16.2123C10.7061 16.0997 10.7693 15.9471 10.7693 15.788V14H12.5693C13.365 14 14.128 13.6839 14.6907 13.1213C15.2533 12.5587 15.5693 11.7957 15.5693 11C15.5693 10.2044 15.2533 9.44129 14.6907 8.87868C14.128 8.31607 13.365 8 12.5693 8ZM12.5693 12.8H10.7693V9.2H12.5693C13.0467 9.2 13.5046 9.38964 13.8421 9.72721C14.1797 10.0648 14.3693 10.5226 14.3693 11C14.3693 11.4774 14.1797 11.9352 13.8421 12.2728C13.5046 12.6104 13.0467 12.8 12.5693 12.8Z"
      fill="currentColor"
      stroke="currentColor"
      stroke-width="0.72"
    />
  </svg></textarea
            >
          </div>
        </div>
        <div class="flex gap-2.5 items-center">
          <button
            type="submit"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Save
          </button>
          <button
            type="button"
            @click="handleClose"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
          >
            Back
          </button>
        </div>
      </form>
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

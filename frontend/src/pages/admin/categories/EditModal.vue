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
          <h1 class="text-3xl font-se font-semibold">Edit Category</h1>
          <div class="flex gap-2 items-center text-sm font-medium">
            <span>Katalog</span>
            <ArrowRight class="size-4 text-neu-500" />
            <RouterLink :to="{ name: 'AdminCategories' }" class="hover:underline"
              >Categories</RouterLink
            >
            <ArrowRight class="size-4 text-neu-500" />
            <span class="text-neu-500">Edit</span>
          </div>
        </div>
        <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col flex-1 gap-3">
          <label for="name" class="text-base font-semibold">Category Name</label>
          <input
            type="text"
            id="name"
            placeholder="Category"
            value="Beach"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
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
            Cancel
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

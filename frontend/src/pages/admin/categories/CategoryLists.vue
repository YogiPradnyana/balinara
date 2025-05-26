<script setup>
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
import CreateModal from './CreateModal.vue'
import { ref, watch } from 'vue'
import EditModal from './EditModal.vue'
const isCreateOpen = ref(false)
const isEditOpen = ref(false)

watch(isCreateOpen, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

watch(isEditOpen, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>
<template>
  <CreateModal v-if="isCreateOpen" @close="isCreateOpen = false" />
  <EditModal v-if="isEditOpen" @close="isEditOpen = false" />
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Categories</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Categories</span>
      </div>
    </div>

    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex flex-col p-4">
        <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
          <div
            class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full"
          >
            <Search class="size-6" />
            <input
              type="text"
              class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
              placeholder="Search something..."
            />
          </div>
          <button
            type="button"
            @click="isCreateOpen = true"
            class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
          >
            <Plus class="size-5" />
            New Category
          </button>
        </div>

        <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">NAME</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-sm text-neu-700 border-b border-neu-100">
                  <td class="p-4 text-neu-900">1</td>
                  <td class="p-4 text-neu-900 font-semibold">Beach</td>
                  <td class="p-4 flex gap-3">
                    <button
                      type="button"
                      @click="isEditOpen = true"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#F0BF05] bg-[#FACA15]"
                    >
                      <Edit class="size-5 text-neu-900" />
                    </button>
                    <button
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                    >
                      <TrashCan class="size-5 text-neu-50" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="flex justify-between items-center mt-3">
          <div class="text-sm text-neu-600">
            Showing <span class="font-medium text-neu-900">1</span> to
            <span class="font-medium text-neu-900">1</span> of
            <span class="font-medium text-neu-900">10</span> Entries
          </div>
          <div class="flex items-center rounded-[8px] overflow-hidden">
            <div class="flex bg-neu-100 text-neu-300 gap-2 h-8 px-3 items-center font-semibold">
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </div>
            <div class="flex bg-neu-100 gap-2 h-8 px-3 cursor-pointer items-center font-semibold">
              Next<ArrowRight2Bold class="size-4" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

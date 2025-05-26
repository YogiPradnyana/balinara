<script setup>
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
</script>
<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Management</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Management</span>
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
          <RouterLink
            :to="{ name: 'AdminUserCreate' }"
            class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
          >
            <Plus class="size-5" />
            New Admin
          </RouterLink>
        </div>

        <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">USERNAME</th>
                  <th class="p-4 text-start font-semibold">EMAIL</th>
                  <th class="p-4 text-start font-semibold">PHONE NUMBER</th>
                  <th class="p-4 text-start font-semibold">ROLE</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-sm text-neu-700 border-b border-neu-100">
                  <td class="p-4 text-neu-900">1</td>
                  <td class="p-4 text-neu-900 font-semibold">Udin Surudin</td>
                  <td class="p-4">udinganteng@gmail.com</td>
                  <td class="p-4">081234567891</td>
                  <td class="p-4">Admin</td>
                  <td class="p-4 flex gap-3">
                    <RouterLink
                      :to="{ name: 'AdminUserEdit', params: { id: 1 } }"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#F0BF05] bg-[#FACA15]"
                    >
                      <Edit class="size-5 text-neu-900" />
                    </RouterLink>
                    <RouterLink
                      :to="{ name: 'AdminUserDetail', params: { id: 1 } }"
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </RouterLink>
                    <button
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                    >
                      <TrashCan class="size-5 text-neu-50" />
                    </button>
                  </td>
                </tr>
                <tr class="text-sm text-neu-700 border-b border-neu-100">
                  <td class="p-4 text-neu-900">2</td>
                  <td class="p-4 text-neu-900 font-semibold">Malik Rumilik</td>
                  <td class="p-4">malik@gmail.com</td>
                  <td class="p-4">081234567892</td>
                  <td class="p-4">Traveler</td>
                  <td class="p-4 flex gap-3">
                    <RouterLink
                      :to="{ name: 'AdminUserDetail', params: { id: 1 } }"
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </RouterLink>
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

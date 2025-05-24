<script setup lang="ts">
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Show from '@/components/icons/Show.vue'
</script>

<template>
  <div class="p-6 space-y-6">
    <div class="flex flex-col">
      <h1 class="text-3xl font-se font-semibold">Detail User</h1>
      <div class="flex gap-2 items-center font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span>Management</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Detail</span>
      </div>
    </div>

    <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col gap-4 md:gap-8">
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-col flex-1 gap-3">
          <label for="name" class="text-base font-semibold">Username</label>
          <input
            type="text"
            id="name"
            disabled
            value="Udin Surudin"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-1 flex-col gap-3">
          <label for="name" class="text-base font-semibold">Email</label>
          <input
            type="text"
            id="name"
            value="udinganteng@gmail.com"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
      </div>
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-1 flex-col gap-3">
          <label for="name" class="text-base font-semibold">Phone Number</label>
          <input
            type="text"
            id="name"
            disabled
            value="081234567891"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col flex-1 gap-3"></div>
      </div>
    </div>

    <div class="flex gap-2.5 items-center">
      <button
        type="button"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#FAFAFA] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        Back
      </button>
    </div>
  </div>
</template>

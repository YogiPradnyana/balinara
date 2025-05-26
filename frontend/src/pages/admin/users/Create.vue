<script setup lang="ts">
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Show from '@/components/icons/Show.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Create Admin</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminUsers' }" class="hover:underline">Management</RouterLink>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Create</span>
      </div>
    </div>

    <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col gap-4 md:gap-8">
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-col flex-1 gap-3">
          <label for="name" class="text-base font-semibold">Username</label>
          <input
            type="text"
            id="name"
            placeholder="Username"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-1 flex-col gap-3">
          <label for="name" class="text-base font-semibold">Email</label>
          <input
            type="text"
            id="name"
            placeholder="Email"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
      </div>
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-1 flex-col gap-3">
          <label for="name" class="text-base font-semibold">Phone Number</label>
          <input
            type="text"
            id="name"
            placeholder="Phone Number"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col flex-1 gap-3">
          <label for="name" class="text-base font-semibold">Password</label>
          <div class="relative flex">
            <input
              type="password"
              class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
              placeholder="Password"
            />
            <Show class="size-5.5 absolute top-1/2 -translate-y-1/2 right-3" />
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-2.5 items-center">
      <button
        type="submit"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
      >
        Create
      </button>
      <RouterLink
        :to="{ name: 'AdminUsers' }"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        Cancel
      </RouterLink>
    </div>
  </div>
</template>

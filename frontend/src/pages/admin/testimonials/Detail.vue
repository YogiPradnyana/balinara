<script setup lang="ts">
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Subtract from '@/components/icons/Subtract.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Detail Review</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminReviews' }" class="hover:underline">Testimonials</RouterLink>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Detail</span>
      </div>
    </div>

    <form class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Form Left -->
      <div
        class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Destination Name</label>
          <input
            type="text"
            id="name"
            value="Gitgit Waterfall"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base font-semibold">Review</label>
          <textarea
            id="descriptions"
            rows="7"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-3xl"
          >
Perfect spot for photography lovers. The temple, ocean, and sunset together create a truly cinematic experience.</textarea
          >
        </div>

        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Photo</label>
          <img
            src="@/assets/images/gitgit-waterfall.webp"
            alt="Ubud Village"
            class="object-cover w-[200px] h-[112px] rounded-2xl"
          />
        </div>
      </div>

      <!-- Form Right -->
      <div
        class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Traveler Name</label>
          <input
            type="text"
            disabled
            value="Udin Surudin"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-gray-300 rounded-full"
          />
        </div>

        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Rating</label>
          <div class="flex gap-1.5 items-center">
            <StarFilled class="size-8" />
            <StarFilled class="size-8" />
            <StarFilled class="size-8" />
            <StarFilled class="size-8" />
            <StarFilled class="size-8" />
          </div>
        </div>
      </div>
    </form>

    <div class="flex gap-2.5 items-center">
      <RouterLink
        :to="{ name: 'AdminReviews' }"
        type="button"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        Back
      </RouterLink>
    </div>
  </div>
</template>

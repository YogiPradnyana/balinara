<script setup>
import DoubleQuotes from '@/components/icons/DoubleQuotes.vue'
import Location from '@/components/icons/Location.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Review</h1>
        <div class="flex flex-col md:flex-row lg:flex-col xl:flex-row gap-5">
          <div v-for="i in 2" :key="i" class="border border-neu-200 rounded-3xl px-6 py-4">
            <div class="flex items-center gap-3 mb-3">
              <img
                src="@/assets/images/gitgit-waterfall.webp"
                class="object-cover size-15 rounded-xl"
              />
              <div class="flex flex-col gap-1.5">
                <h3 class="font-semibold">Gitgit Waterfall</h3>
                <div class="flex gap-1 items-center">
                  <Location class="size-5" />
                  <p class="text-sm font-medium">Sukasada, Buleleng</p>
                </div>
              </div>
            </div>
            <div class="space-y-2">
              <DoubleQuotes class="size-6 sm:size-7" />
              <p class="text-sm sm:text-base text-neu-600">
                Perfect spot for photography lovers. The temple, ocean, and sunset together create a
                truly cinematic experience.
              </p>
              <div class="flex gap-1 items-center">
                <StarFilled class="size-5 sm:size-6" />
                <StarFilled class="size-5 sm:size-6" />
                <StarFilled class="size-5 sm:size-6" />
                <StarFilled class="size-5 sm:size-6" />
                <StarFilled class="size-5 sm:size-6" />
              </div>
            </div>
            <div class="flex items-center gap-2 mt-3">
              <img
                src="@/assets/images/User Avatar.jpg"
                alt="User"
                class="object-cover size-10.5 rounded-full"
              />
              <span class="text-sm font-medium">Udin Surudin</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

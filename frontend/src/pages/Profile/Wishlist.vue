<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import HeartFilled from '@/components/icons/HeartFilled.vue'
import Location from '@/components/icons/Location.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">
          Wishlist
        </h1>
        <div class="flex gap-5 flex-wrap">
          <div
            v-for="i in 4"
            :key="i"
            class="flex flex-col border w-full sm:w-84 lg:w-72 cursor-pointer hover:scale-102 transition-all duration-500 ease-in-out border-neu-100 rounded-3xl gap-3 p-3"
          >
            <div class="relative h-43 w-full">
              <img
                src="@/assets/images/mount-agung.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-2xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-xs bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                >
                  Mount Agung
                  <ArrowUpRight class="size-4" />
                </div>
                <div class="flex items-center justify-between w-full">
                  <div
                    class="py-1 px-2.5 flex items-center justify-center font-medium text-sm gap-1 bg-sur-50 rounded-full"
                  >
                    <StarFilled class="size-4.5" />
                    4.8
                  </div>
                  <div class="p-2 flex items-center justify-center bg-sur-50 rounded-full">
                    <HeartFilled class="size-5 text-neu-900" />
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base text-neu-900 font-semibold">Mount Agung</h3>
              <div class="gap-1 font-medium text-sm items-center mt-1 flex">
                <Location class="size-4.5" />Bebandem, Karangasem
              </div>
              <p class="text-sm text-neu-600 mt-3 line-clamp-2">
                Mount Agung is Bali's highest and most sacred mountain, presenting a challenging
                trek with stunning vistas and significant spiritual importance to the Balinese
                people.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

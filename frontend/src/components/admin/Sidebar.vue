<script setup>
import Heart from '@/components/icons/Heart.vue'
import Home from '@/components/icons/Home.vue'
import MapPin from '@/components/icons/MapPin.vue'
import Message from '@/components/icons/Message.vue'
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
import Tag from '@/components/icons/Tag.vue'
import Users from '@/components/icons/Users.vue'
</script>
<template>
  <div class="min-w-64 flex flex-col gap-10 p-4 min-h-screen bg-sur-50 border-r border-neu-200">
    <h1 class="text-2xl font-se font-semibold pl-3">Bali<span class="text-pr-500">nara</span></h1>
    <div class="space-y-4 text-sm">
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Master</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center text-pr-500 py-2 px-4 font-medium bg-[#EFF6F2] hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Home class="text-pr-500 size-5" />Dashboard
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">User</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Users class="text-neu-500 size-5" />Management
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Katalog</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <OutlinedLocation class="text-neu-500 size-5" />Destinations
        </RouterLink>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Tag class="text-neu-500 size-5" />Categories
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">REVIEWS</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Message class="text-neu-500 size-5" />Testimonials
        </RouterLink>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex justify-between items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <span class="flex items-center gap-3"
            ><MapPin class="text-neu-500 size-5" />Suggested Spot</span
          ><span
            class="flex items-center text-neu-50 text-sm rounded-[6px] justify-center px-2 bg-pr-500"
            >2</span
          >
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import Home from '@/components/icons/Home.vue'
import MapPin from '@/components/icons/MapPin.vue'
import Message from '@/components/icons/Message.vue'
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
import Tag from '@/components/icons/Tag.vue'
import Users from '@/components/icons/Users.vue'
import Parking from '../icons/facilities/Parking.vue'

const props = defineProps({
  isSidebarOpen: Boolean,
})
</script>
<template>
  <aside
    class="fixed top-0 left-0 z-999 min-w-64 mt-16 lg:mt-0 -translate-x-full lg:translate-x-0 flex flex-col gap-6 sm:gap-8 p-4 min-h-screen bg-sur-50 border-r border-neu-200 transition-all duration-300 ease-in-out"
    :class="[isSidebarOpen ? 'translate-x-0' : '']"
  >
    <RouterLink
      :to="{ name: 'Home' }"
      class="text-2xl sm:text-3xl font-se font-semibold pl-3 pt-2 sm:pt-4"
    >
      Bali<span class="text-pr-500">nara</span>
    </RouterLink>
    <div class="space-y-4 text-sm">
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Master</h3>
        <RouterLink
          :to="{ name: 'Dashboard' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.name === 'Dashboard' ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <Home
            class="size-5"
            :class="$route.name === 'Dashboard' ? ' text-pr-500' : 'text-neu-500'"
          />Dashboard
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">User</h3>
        <RouterLink
          :to="{ name: 'AdminUsers' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/users') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <Users
            class="size-5"
            :class="$route.path.startsWith('/admin/users') ? ' text-pr-500' : 'text-neu-500'"
          />Management
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Katalog</h3>
        <RouterLink
          :to="{ name: 'AdminDestinations' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/destinations') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <OutlinedLocation
            class="size-5"
            :class="$route.path.startsWith('/admin/destinations') ? ' text-pr-500' : 'text-neu-500'"
          />Destinations
        </RouterLink>
        <RouterLink
          :to="{ name: 'AdminCategories' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/categories') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <Tag
            class="size-5"
            :class="$route.path.startsWith('/admin/categories') ? ' text-pr-500' : 'text-neu-500'"
          />Categories
        </RouterLink>
        <RouterLink
          :to="{ name: 'AdminFacilities' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/facilities') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <Parking
            class="size-5"
            :class="$route.path.startsWith('/admin/facilities') ? ' text-pr-500' : 'text-neu-500'"
          />Facilities
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">REVIEWS</h3>
        <RouterLink
          :to="{ name: 'AdminReviews' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/reviews') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <Message
            class="size-5"
            :class="$route.path.startsWith('/admin/reviews') ? ' text-pr-500' : 'text-neu-500'"
          />Testimonials
        </RouterLink>
        <RouterLink
          :to="{ name: 'AdminSuggestions' }"
          class="flex justify-between items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          :class="$route.path.startsWith('/admin/suggestions') ? 'bg-[#EFF6F2] text-pr-500' : ''"
        >
          <span class="flex items-center gap-3"
            ><MapPin
              class="size-5"
              :class="
                $route.path.startsWith('/admin/suggestions') ? ' text-pr-500' : 'text-neu-500'
              "
            />Suggested Spot</span
          ><span
            class="flex items-center text-neu-50 text-sm rounded-[6px] justify-center px-2 bg-pr-500"
            >2</span
          >
        </RouterLink>
      </div>
    </div>
  </aside>
</template>

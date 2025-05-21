<script setup>
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
import Star from '@/components/icons/Star.vue'
import Heart from '@/components/icons/Heart.vue'
import User from '@/components/icons/User.vue'
</script>
<template>
  <aside
    class="hidden lg:block min-w-56 xl:min-w-70 h-140 border-neu-200 border-r bg-sur-50 rounded-3xl p-4"
  >
    <div class="flex flex-col gap-6">
      <div class="gap-2 flex flex-col xl:flex-row items-center">
        <img
          src="@/assets/images/User Avatar.jpg"
          alt="User Profile"
          class="size-12 rounded-full"
        />
        <div class="flex flex-col items-center xl:items-start gap-[2px]">
          <p class="font-semibold whitespace-nowrap text-xs md:text-sm">Udin Surudin</p>
          <p class="text-sm text-neu-500">udinganteng@gmail.com</p>
        </div>
      </div>
      <ul class="flex flex-col gap-2">
        <li>
          <RouterLink
            :to="{ name: 'Profile' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          >
            <User class="text-neu-500 size-5" />Profile
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'Wishlist' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium bg-[#EFF6F2] hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          >
            <Heart class="text-pr-500 size-5" />Wishlist
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'UserReview' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          >
            <Star class="text-neu-500 size-5" />Review
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'UserSuggestion' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
          >
            <OutlinedLocation class="text-neu-500 size-5" />Suggest
          </RouterLink>
        </li>
      </ul>
    </div>
  </aside>
</template>

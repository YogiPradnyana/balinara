<script setup>
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
import Star from '@/components/icons/Star.vue'
import Heart from '@/components/icons/Heart.vue'
import User from '@/components/icons/User.vue'
import { useAuthStore } from '@/stores/authStore'
import defaultAvatar from '@/assets/images/user_profile/default-avatar.png'

const authStore = useAuthStore()
</script>
<template>
  <aside class="hidden lg:block min-w-56 xl:min-w-70 h-140 border-neu-100 border-r bg-sur-50 p-4">
    <div class="flex flex-col gap-6">
      <div class="gap-2 flex flex-col xl:flex-row items-center">
        <img
          v-if="authStore.currentUser?.image"
          :src="authStore.currentUser.image"
          alt="User Profile"
          class="size-12 object-cover rounded-full border-2 border-gray-200"
        />
        <img
          v-else
          :src="defaultAvatar"
          alt="Default Profile"
          class="size-12 rounded-full border border-neu-200 object-cover"
        />
        <div class="flex flex-col items-center xl:items-start gap-[2px]">
          <p class="font-medium whitespace-nowrap text-xs md:text-sm">
            {{ authStore.currentUser.username }}
          </p>
          <p class="text-sm text-neu-500">{{ authStore.currentUser.email }}</p>
        </div>
      </div>
      <ul class="flex flex-col gap-2">
        <li>
          <RouterLink
            :to="{ name: 'Profile' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            :class="$route.path.startsWith('/user/profile') ? 'bg-[#EFF6F2] text-pr-500' : ''"
          >
            <User
              class="size-5"
              :class="$route.path.startsWith('/user/profile') ? ' text-pr-500' : 'text-neu-500'"
            />Profile
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'Wishlist' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            :class="$route.path.startsWith('/user/wishlist') ? 'bg-[#EFF6F2] text-pr-500' : ''"
          >
            <Heart
              class="size-5"
              :class="$route.path.startsWith('/user/wishlist') ? ' text-pr-500' : 'text-neu-500'"
            />Wishlist
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'UserReview' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            :class="$route.path.startsWith('/user/reviews') ? 'bg-[#EFF6F2] text-pr-500' : ''"
          >
            <Star
              class="size-5"
              :class="$route.path.startsWith('/user/reviews') ? ' text-pr-500' : 'text-neu-500'"
            />Review
          </RouterLink>
        </li>
        <li>
          <RouterLink
            :to="{ name: 'UserSuggestion' }"
            class="flex gap-3 items-center py-2.5 px-2 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            :class="$route.path.startsWith('/user/suggestions') ? 'bg-[#EFF6F2] text-pr-500' : ''"
          >
            <OutlinedLocation
              class="size-5"
              :class="$route.path.startsWith('/user/suggestions') ? ' text-pr-500' : 'text-neu-500'"
            />Suggest
          </RouterLink>
        </li>
      </ul>
    </div>
  </aside>
</template>

<script setup>
import ArrowDown from '@/components/icons/ArrowDown.vue'
import HamburgerMenu from '../icons/HamburgerMenu.vue'
import Exit from '../icons/Exit.vue'
import defaultAvatar from '@/assets/images/user_profile/default-avatar.png'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

const props = defineProps({
  isSidebarOpen: Boolean,
})

const emit = defineEmits(['sidebarOpen'])

const handleSidebar = () => {
  emit('sidebarOpen')
}
</script>
<template>
  <div
    class="sticky top-0 w-full z-99999 flex justify-between lg:justify-end items-center p-3.5 bg-sur-50 border-b border-neu-200"
  >
    <div class="lg:hidden transform transition-transform duration-500 ease-in-out">
      <button
        @click="handleSidebar"
        class="cursor-pointer flex items-center justify-center p-2.5 rounded-lg"
        :class="[isSidebarOpen == false ? '' : 'bg-[#F5F5F5]']"
        aria-label="Toggle sidebar"
      >
        <HamburgerMenu v-if="isSidebarOpen == false" class="text-neu-600 size-4.5" />
        <Exit v-else class="text-neu-600 size-4.5" />
      </button>
    </div>
    <div class="gap-3 w-fit flex items-center">
      <img
        v-if="authStore.currentUser?.image"
        :src="authStore.currentUser.image"
        alt="User Profile"
        class="size-9 object-cover rounded-full border-2 border-neu-200"
      />
      <img
        v-else
        :src="defaultAvatar"
        alt="Default Profile"
        class="size-9 rounded-full border-2 border-neu-200 object-cover"
      />
      <p class="text-neu-900 gap-0.5 flex items-center font-medium text-sm max-w-36 line-clamp-1">
        <span class="hidden sm:block">{{ authStore.currentUser.username }}</span
        ><ArrowDown class="text-neu-900" />
      </p>
    </div>
  </div>
</template>

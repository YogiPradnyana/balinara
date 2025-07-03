<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import HeartFilled from '@/components/icons/HeartFilled.vue'
import Location from '@/components/icons/Location.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Sidebar from '@/components/Sidebar.vue'
import { useAuthStore } from '@/stores/authStore'
import { useWishlistStore } from '@/stores/wishlistStore'
import { onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import {
  showNotification,
  showConfirmationToast,
  dismissCurrentConfirmationToast,
} from '@/services/notificationService'
import ConfirmationToast from '@/components/ConfirmationToast.vue'

const authStore = useAuthStore()
const wishlistStore = useWishlistStore()

const router = useRouter()

// const handleRemoveFromWishlist = async (destinationId) => {
//   if (confirm('Apakah Anda yakin ingin menghapus dari wishlist?')) {
//     await wishlistStore.remove(destinationId)
//   }
// }

const handleRemoveFromWishlist = (destinationId) => {
  const message = `Are you sure you want to delete from wishlist?`
  const onConfirm = async () => {
    try {
      await wishlistStore.remove(destinationId)
      showNotification('success', 'Deleted from wishlist')
    } catch (error) {
      showNotification('error', 'Failed to delete destination.')
    }
    dismissCurrentConfirmationToast()
  }
  showConfirmationToast(
    h(ConfirmationToast, { message, onConfirm, onCancel: dismissCurrentConfirmationToast }),
  )
}

const viewDestinationDetail = (slug) => {
  router.push({ name: 'DetailDestination', params: { slug: slug } })
}

function formatAddress(address) {
  if (!address) {
    return 'N/A'
  }
  // Menggabungkan bagian alamat menjadi satu string yang rapi
  const parts = [address.district, address.regency]
  return parts.filter((part) => part).join(', ') // filter(part => part) untuk menghapus bagian yang kosong
}

// Ambil data wishlist saat komponen pertama kali dimuat
onMounted(() => {
  if (authStore.isAuthenticated) {
    wishlistStore.fetchWishlist()
  }
})
</script>
<template>
  <div
    v-if="authStore.isAuthenticated && authStore.currentUser"
    class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30"
  >
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 w-full lg:p-4">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">
          Wishlist
        </h1>
        <div
          v-if="wishlistStore.items.length === 0"
          class="text-center py-10 px-6 w-full rounded-lg"
        >
          <p class="text-gray-500">Your wishlist is still empty.</p>
          <p class="text-gray-400 text-sm mt-2">
            Find a destination and click the heart button to save it here.
          </p>
        </div>
        <div v-else class="flex gap-5 flex-wrap">
          <div
            v-for="item in wishlistStore.items"
            :key="item.destination.id"
            @click="viewDestinationDetail(item.destination.slug)"
            class="flex flex-col border w-full sm:w-84 lg:w-72 cursor-pointer hover:scale-102 transition-all duration-500 ease-in-out border-neu-100 rounded-3xl gap-3 p-3"
          >
            <div class="relative h-43 w-full">
              <img
                :src="item.destination.primary_image_url"
                :alt="item.destination.name"
                class="object-cover w-full h-full rounded-2xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-xs bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                >
                  {{ item.destination.name }}
                  <ArrowUpRight class="size-4" />
                </div>
                <div class="flex items-center justify-between w-full">
                  <div
                    class="py-1 px-2.5 flex items-center justify-center font-medium text-sm gap-1 bg-sur-50 rounded-full"
                  >
                    <StarFilled class="size-4.5" />
                    {{ item.destination.average_rating }}
                  </div>
                  <button
                    @click.prevent.stop="handleRemoveFromWishlist(item.destination.id)"
                    class="p-2 flex items-center justify-center cursor-pointer bg-sur-50 rounded-full"
                  >
                    <HeartFilled class="size-5 text-neu-900" />
                  </button>
                </div>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base text-neu-900 font-semibold">{{ item.destination.name }}</h3>
              <div class="gap-1 font-medium text-sm items-center mt-1 flex">
                <Location class="size-4.5" />{{ formatAddress(item.destination.address) }}
              </div>
              <p class="text-sm text-neu-600 mt-3 line-clamp-2">
                {{ item.destination.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

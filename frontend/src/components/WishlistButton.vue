<script setup>
import { useWishlistStore } from '@/stores/wishlistStore'
import HeartFilled from '@/components/icons/HeartFilled.vue' // Anda sudah punya ini
import HeartOutline from '@/components/icons/Heart.vue' // Anda mungkin perlu membuat ikon ini
import { showNotification } from '@/services/notificationService'

// 1. Terima ID destinasi sebagai 'prop' dari komponen induk
const props = defineProps({
  destinationId: {
    type: Number,
    required: true,
  },
  isIcon: {
    type: Boolean,
    required: true,
  },
})

// 2. Gunakan wishlist store
const wishlistStore = useWishlistStore()

// 3. Buat fungsi untuk menangani klik
const toggleWishlist = () => {
  if (wishlistStore.isWishlisted(props.destinationId)) {
    // Jika sudah ada, panggil fungsi remove
    wishlistStore.remove(props.destinationId)
    showNotification('success', 'Deleted from wishlist')
  } else {
    // Jika belum ada, panggil fungsi add
    wishlistStore.add(props.destinationId)
    showNotification('success', 'Added to wishlist')
  }
}
</script>

<template>
  <button
    v-if="isIcon"
    @click.prevent.stop="toggleWishlist"
    class="p-2 sm:p-2.5 flex items-center justify-center cursor-pointer bg-sur-50 rounded-full z-10"
    aria-label="Toggle Wishlist"
  >
    <HeartFilled
      v-if="wishlistStore.isWishlisted(props.destinationId)"
      class="size-5 sm:size-6 text-neu-900"
    />
    <HeartOutline v-else class="size-5 sm:size-6 text-neu-900" />
  </button>
  <button
    v-else
    @click.prevent.stop="toggleWishlist"
    class="px-2 sm:px-4 border-neu-200 text-sm sm:text-base border-[1.6px] gap-2 py-2 rounded-full font-medium items-center flex cursor-pointer"
  >
    <HeartFilled
      v-if="wishlistStore.isWishlisted(props.destinationId)"
      class="size-5 sm:size-6 text-neu-900"
    />
    <HeartOutline v-else class="size-5 sm:size-6 text-neu-900" />
    <span class="hidden sm:block">Save</span>
  </button>
</template>

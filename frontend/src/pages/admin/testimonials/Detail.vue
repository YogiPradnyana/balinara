<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'
import StarRatingDisplay from '@/components/StarRatingDisplay.vue' // Pastikan komponen ini diimpor
import ArrowRight from '@/components/icons/ArrowRight.vue'
import { useUiStore } from '@/stores/uiStore'

const route = useRoute()
const reviewStore = useReviewStore()
const uiStore = useUiStore()

// Computed properties untuk mendapatkan data dari store
const review = computed(() => reviewStore.currentReview)
const isLoading = computed(() => reviewStore.isLoading)

function openImageModal(reviewImages, clickedImageIndex) {
  const imageUrls = reviewImages.map((img) => img.image)
  uiStore.openLightbox(imageUrls, clickedImageIndex)
}

// Saat komponen dimuat, ambil ID dari URL dan fetch datanya
onMounted(() => {
  const reviewId = route.params.id
  if (reviewId) {
    reviewStore.fetchReviewById(reviewId)
  }
})
</script>

<template>
  <div v-if="isLoading" class="text-center p-10">Loading review details...</div>

  <div v-else-if="!review" class="text-center p-10">Review not found or could not be loaded.</div>

  <div v-else class="space-y-6">
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

    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <div
        class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Destination Name</label>
          <input
            type="text"
            :value="review.destination.name"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Review Comment</label>
          <textarea
            rows="7"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-neu-200 rounded-3xl whitespace-pre-wrap"
            >{{ review.comment }}</textarea
          >
        </div>

        <div v-if="review.images && review.images.length > 0" class="flex flex-col gap-3">
          <label class="text-base font-semibold">Photos</label>
          <div class="flex flex-wrap gap-2">
            <img
              v-for="(img, index) in review.images"
              :key="img.id"
              :src="img.image"
              @click="openImageModal(review.images, index)"
              :alt="`Review image for ${review.destination.name}`"
              class="object-cover w-48 h-28 rounded-xl"
            />
          </div>
        </div>
      </div>

      <div
        class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Traveler Name</label>
          <input
            type="text"
            :value="review.user.username"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-gray-300 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Rating</label>
          <div class="flex gap-1.5 items-center">
            <StarRatingDisplay :rating="review.rating" star-size="size-8" />
          </div>
        </div>
      </div>
    </div>

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

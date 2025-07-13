<script setup>
import DoubleQuotes from '@/components/icons/DoubleQuotes.vue'
import defaultAvatar from '@/assets/images/user_profile/default-avatar.png'
import Location from '@/components/icons/Location.vue'
import Sidebar from '@/components/Sidebar.vue'
import StarRatingDisplay from '@/components/StarRatingDisplay.vue'
import { useAuthStore } from '@/stores/authStore'
import { useReviewStore } from '@/stores/reviewStore'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUiStore } from '@/stores/uiStore'

const authStore = useAuthStore()
const reviewStore = useReviewStore()
const router = useRouter()
const uiStore = useUiStore()

const myReviews = computed(() => reviewStore.myReviews)
const isLoading = computed(() => reviewStore.isLoading)

function openImageModal(reviewImages, clickedImageIndex) {
  const imageUrls = reviewImages.map((img) => img.image)
  uiStore.openLightbox(imageUrls, clickedImageIndex)
}

onMounted(() => {
  reviewStore.fetchMyReviews()
})

// Fungsi untuk navigasi ke halaman detail destinasi
const viewDestinationDetail = (slug) => {
  router.push({ name: 'DetailDestination', params: { slug: slug } })
}
</script>
<template>
  <VueEasyLightbox
    :visible="isModalVisible"
    :imgs="modalImages"
    :index="modalIndex"
    @hide="closeImageModal"
  />
  <div
    v-if="authStore.isAuthenticated && authStore.currentUser"
    class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30"
  >
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4 flex-1">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Review</h1>
        <div v-if="isLoading" class="text-center py-10">Loading your reviews...</div>
        <div v-else-if="myReviews.length > 0" class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div
            v-for="review in myReviews"
            :key="review.id"
            class="border border-neu-200 rounded-3xl px-6 py-4"
          >
            <div
              @click="viewDestinationDetail(review.destination.slug)"
              class="flex items-center gap-3 mb-3 cursor-pointer group"
            >
              <img
                :src="review.destination.primary_image_url || 'https://placehold.co/60x60'"
                alt="Destination Image"
                class="object-cover size-15 rounded-xl"
              />
              <div class="flex flex-col gap-1.5">
                <h3 class="font-semibold">{{ review.destination.name }}</h3>
                <div class="flex gap-1 items-center">
                  <Location class="size-5" />
                  <p class="text-sm font-medium">
                    {{ review.destination.address.district }},
                    {{ review.destination.address.regency }}
                  </p>
                </div>
              </div>
            </div>
            <div class="space-y-2">
              <DoubleQuotes class="size-6 sm:size-7" />
              <p class="text-sm sm:text-base text-neu-600 whitespace-pre-wrap">
                {{ review.comment }}
              </p>

              <div
                v-if="review.images && review.images.length > 0"
                class="mt-4 flex gap-2 flex-wrap"
              >
                <div
                  v-for="(img, index) in review.images.slice(0, 4)"
                  :key="img.id"
                  class="relative"
                >
                  <img
                    :src="img.image"
                    alt="User review image"
                    class="size-16 sm:size-20 rounded-lg object-cover cursor-pointer"
                    :class="{ 'brightness-50': index === 3 && review.images.length > 4 }"
                    @click="openImageModal(review.images, index)"
                  />

                  <div
                    v-if="index === 3 && review.images.length > 4"
                    class="absolute inset-0 flex items-center justify-center text-white font-medium cursor-pointer"
                  >
                    +{{ review.images.length - 4 }}
                  </div>
                </div>
              </div>

              <div class="flex gap-1 items-center">
                <StarRatingDisplay :rating="review.rating" />
              </div>
            </div>
            <div class="flex items-center gap-2 mt-3">
              <img
                :src="review.user.image_url || defaultAvatar"
                alt="User"
                class="object-cover size-10.5 rounded-full"
              />
              <span class="text-sm font-medium"> {{ review.user.username }}</span>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-20 bg-gray-50 rounded-2xl">
          <p class="text-neu-600">You haven't written any reviews yet.</p>
          <RouterLink
            :to="{ name: 'WriteReview' }"
            class="text-pr-500 font-semibold mt-2 inline-block hover:underline"
          >
            Write your first review!
          </RouterLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, h } from 'vue'
import { RouterLink } from 'vue-router'
import { useReviewStore } from '@/stores/reviewStore'
import {
  showNotification,
  showConfirmationToast,
  dismissCurrentConfirmationToast,
} from '@/services/notificationService'
import ConfirmationToast from '@/components/ConfirmationToast.vue'

import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import StarRatingDisplay from '@/components/StarRatingDisplay.vue'
import TrashCan from '@/components/icons/TrashCan.vue'

const reviewStore = useReviewStore()

const reviews = computed(() => reviewStore.reviews)
const pagination = computed(() => reviewStore.pagination)
const isLoading = computed(() => reviewStore.isLoading)

const queryParams = ref({
  page: 1,
  search: '',
})

const fetchReviewsWithParams = () => {
  reviewStore.fetchAllReviews(queryParams.value)
}

onMounted(() => {
  fetchReviewsWithParams()
})

const ITEMS_PER_PAGE = 10 // Sesuaikan dengan pengaturan paginasi di backend

// Computed properties untuk teks paginasi
const firstItemNumber = computed(() => {
  if (pagination.value.count === 0) return 0
  return (queryParams.value.page - 1) * ITEMS_PER_PAGE + 1
})
const lastItemNumber = computed(() => {
  const last = queryParams.value.page * ITEMS_PER_PAGE
  return Math.min(last, pagination.value.count)
})

// Watcher dengan debounce untuk search bar
let searchTimeout = null
watch(
  () => queryParams.value.search,
  () => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      queryParams.value.page = 1 // Selalu reset ke halaman 1 saat search baru
      fetchReviewsWithParams()
    }, 500) // Debounce 500ms
  },
)

// Fungsi Delete dengan konfirmasi toast
const confirmDelete = (review) => {
  const message = `Are you sure you want to delete the review for "${review.destination.name}" by "${review.user.username}"? This action cannot be undone.`
  const onConfirm = async () => {
    try {
      await reviewStore.deleteReview(review.id)
      // Jika item terakhir di halaman dihapus, kembali ke halaman sebelumnya
      if (reviews.value.length === 0 && queryParams.value.page > 1) {
        queryParams.value.page--
      }
      fetchReviewsWithParams() // Muat ulang data
    } catch (error) {
      showNotification('error', reviewStore.error || 'Failed to delete review.')
    }
    dismissCurrentConfirmationToast()
  }
  showConfirmationToast(
    h(ConfirmationToast, { message, onConfirm, onCancel: dismissCurrentConfirmationToast }),
  )
}

// Fungsi untuk penomoran baris
const calculateItemNumber = (indexInPage) => {
  return (queryParams.value.page - 1) * ITEMS_PER_PAGE + indexInPage + 1
}

// Fungsi untuk navigasi halaman
const goToPage = (pageNumber) => {
  if (pageNumber >= 1 && pageNumber <= Math.ceil(pagination.value.count / ITEMS_PER_PAGE)) {
    queryParams.value.page = pageNumber
    fetchReviewsWithParams()
  }
}

const goToNextPage = () => {
  if (pagination.value.next) {
    goToPage(queryParams.value.page + 1)
  }
}

const goToPrevPage = () => {
  if (pagination.value.previous) {
    goToPage(queryParams.value.page - 1)
  }
}
</script>
<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Testimonials</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Testimonials</span>
      </div>
    </div>

    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex flex-col p-4">
        <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
          <div
            class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full"
          >
            <Search class="size-6" />
            <input
              type="text"
              v-model="queryParams.search"
              class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
              placeholder="Search by destination, or traveler..."
            />
          </div>
        </div>

        <div v-if="isLoading && reviews.length === 0" class="text-center py-12">
          <p class="text-gray-500">Loading reviews...</p>
        </div>

        <div
          v-else-if="reviews.length > 0"
          class="mt-4 overflow-hidden border border-neu-100 rounded-2xl"
        >
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">DESTINATION NAME</th>
                  <th class="p-4 text-start font-semibold">TRAVELER NAME</th>
                  <th class="p-4 text-start font-semibold">RATING</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(review, index) in reviews"
                  :key="review.id"
                  class="text-sm text-neu-700 border-b border-neu-100"
                >
                  <td class="p-4 text-neu-900">{{ calculateItemNumber(index) }}</td>
                  <td class="p-4 text-neu-900 font-semibold">{{ review.destination.name }}</td>
                  <td class="p-4">{{ review.user.username }}</td>
                  <td class="p-4">
                    <div class="flex gap-1.5 items-center">
                      <StarRatingDisplay :rating="review.rating" />
                    </div>
                  </td>
                  <td class="p-4 flex gap-3">
                    <RouterLink
                      :to="{ name: 'AdminReviewDetail', params: { id: review.id } }"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </RouterLink>
                    <button
                      type="button"
                      @click="confirmDelete(review)"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                    >
                      <TrashCan class="size-5 text-neu-50" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="text-center py-12 text-gray-500">No reviews found.</div>

        <div
          v-if="pagination.count > 0"
          class="flex justify-between items-center gap-3 flex-wrap mt-3"
        >
          <div class="text-sm text-neu-600">
            Showing <span class="font-medium text-neu-900">{{ firstItemNumber }}</span> to
            <span class="font-medium text-neu-900">{{ lastItemNumber }}</span> of
            <span class="font-medium text-neu-900">{{ pagination.count }}</span> Entries
          </div>
          <div class="flex items-center rounded-[8px] overflow-hidden">
            <button
              @click="goToPrevPage"
              :disabled="!pagination.previous"
              :class="[
                'flex bg-neu-100 gap-2 h-8 px-3 items-center font-semibold transition-colors',
                pagination.previous ? 'cursor-pointer hover:bg-neu-200' : 'text-neu-300 ',
              ]"
              aria-label="Prev Page"
            >
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </button>
            <button
              @click="goToNextPage"
              :disabled="!pagination.next"
              :class="[
                'flex bg-neu-100 gap-2 h-8 px-3 items-center font-semibold transition-colors',
                pagination.next ? 'cursor-pointer hover:bg-neu-200' : 'text-neu-300 ',
              ]"
              aria-label="Next Page"
            >
              Next<ArrowRight2Bold class="size-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDestinationStore } from '@/stores/destinationStore'
import { useReviewStore } from '@/stores/reviewStore' // Asumsi Anda sudah membuat store ini
import { useAuthStore } from '@/stores/authStore'
import { showNotification } from '@/services/notificationService'
import mainImage from '@/assets/images/tegalallang-rice-terraces.webp'
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Location from '@/components/icons/Location.vue'
import Photo from '@/components/icons/Photo.vue'
import Search from '@/components/icons/Search.vue'
import Star from '@/components/icons/Star.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import SuccessNotification from '@/components/SuccessNotification.vue'

const route = useRoute()
const router = useRouter()
const destinationStore = useDestinationStore()
const reviewStore = useReviewStore()
const authStore = useAuthStore()

const selectedDestination = ref(null)

// State untuk form review
const reviewData = ref({
  destination: null, // Akan diisi dengan ID destinasi
  rating: 0,
  comment: '',
  image_ids: [],
})

// State untuk logika search destinasi
const searchTerm = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const isSearchFocused = ref(false)
const tempImages = ref([]) // State untuk menampilkan thumbnail
const isUploading = ref(false)

// State untuk UI
const hoverRating = ref(0)

// Computed property untuk mengosongkan search result saat tidak fokus
const displayedSearchResults = computed(() => {
  return isSearchFocused.value ? searchResults.value : []
})

let searchTimeout
watch(searchTerm, (newQuery) => {
  searchResults.value = [] // Kosongkan hasil lama
  if (!newQuery) return

  isSearching.value = true
  clearTimeout(searchTimeout)

  searchTimeout = setTimeout(async () => {
    // Gunakan action yang sudah ada, tapi simpan hasilnya secara lokal
    const response = await destinationStore.fetchDestinations({ search: newQuery, page_size: 5 })
    searchResults.value = destinationStore.destinations
    isSearching.value = false
  }, 500)
})

// Fungsi yang berjalan saat pengguna memilih destinasi dari hasil pencarian
function selectDestination(destination) {
  selectedDestination.value = destination
  reviewData.value.destination = destination.id
  searchTerm.value = destination.name // Isi search bar dengan nama destinasi
  isSearchFocused.value = false // Tutup dropdown hasil pencarian
}

// Fungsi untuk memberikan rating bintang
function setRating(rating) {
  reviewData.value.rating = rating
}

async function handleImageUpload(event) {
  const files = Array.from(event.target.files)
  event.target.value = null

  if (files.length === 0) return

  isUploading.value = true
  for (const file of files) {
    try {
      const tempImage = await reviewStore.uploadTemporaryReviewImage(file)
      tempImages.value.push(tempImage) // Tampilkan thumbnail
      reviewData.value.image_ids.push(tempImage.id) // Simpan ID untuk dikirim
    } catch (error) {
      showNotification('error', `Failed to upload ${file.name}`)
    }
  }
  isUploading.value = false
}

function removeTempImage(imageToRemove) {
  tempImages.value = tempImages.value.filter((img) => img.id !== imageToRemove.id)
  reviewData.value.image_ids = reviewData.value.image_ids.filter((id) => id !== imageToRemove.id)
  // TODO: Opsional, panggil API untuk hapus file fisik dari server jika perlu
}

// Fungsi utama saat tombol "Post My Review" ditekan
async function handleSubmit() {
  // 1. Cek apakah user sudah login
  if (!authStore.isAuthenticated) {
    authStore.showLoginModal = true
    return
  }

  // 2. Cek apakah destinasi sudah dipilih
  if (!reviewData.value.destination) {
    showNotification('error', 'Please select a destination first.')
    return
  }

  // 3. Validasi form sederhana
  if (reviewData.value.rating === 0 || !reviewData.value.comment.trim()) {
    showNotification('error', 'Please provide a rating and a comment.')
    return
  }

  try {
    await reviewStore.createReview(reviewData.value)
    showNotification('success', 'Thank you! Your review has been submitted.')

    // Arahkan kembali ke halaman detail setelah berhasil
    router.push({
      name: 'DetailDestination',
      params: { slug: selectedDestination.value.slug },
    })
  } catch (error) {
    const errorMessage =
      error.response?.data?.detail ||
      'Failed to submit review. You may have already reviewed this place.'
    showNotification('error', errorMessage)
  }
}

// Logika untuk menangani klik di luar area search agar dropdown tertutup
const searchFormRef = ref(null)
onMounted(() => {
  // Jika datang dari halaman detail, langsung pilih destinasinya
  const slug = route.params.slug
  if (slug) {
    destinationStore.fetchDestinationBySlug(slug).then(() => {
      selectDestination(destinationStore.currentDestination)
    })
  }

  // Event listener untuk klik di luar
  const handleClickOutside = (event) => {
    if (searchFormRef.value && !searchFormRef.value.contains(event.target)) {
      isSearchFocused.value = false
    }
  }
  document.addEventListener('click', handleClickOutside)
  onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
  })
})
</script>
<template>
  <!-- <SuccessNotification v-if="isSuccessOpen" @close="isSuccessOpen = false" /> -->
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <div class="relative w-full h-124 xs:h-[380px] rounded-3xl mt-10 md:mt-16">
      <img :src="mainImage" alt="" class="object-cover w-full h-full rounded-3xl overflow-hidden" />
      <div class="flex flex-col w-full justify-between absolute bottom-0 top-0 left-0 p-4 md:p-6">
        <div
          class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full"
        >
          Tegallallang Rice Terraces
          <ArrowUpRight class="size-4" />
        </div>
        <div class="flex-col flex items-center gap-2.5">
          <h1
            class="text-[40px] text-neu-50 md:text-[48px] max-w-160 text-center font-semibold leading-14 md:leading-[62px] font-se"
          >
            Help Future Travelers with Your Insight
          </h1>
          <div class="max-w-[640px] relative w-full h-[52px]">
            <div
              ref="searchFormRef"
              @click="handleFormClick"
              class="absolute w-full flex outline bg-sur-50 outline-neu-200 p-1.5"
              :class="[
                isSearchFocused
                  ? ' rounded-3xl flex-col'
                  : 'justify-between  flex-row items-center rounded-full',
              ]"
            >
              <div class="wrapper gap-2 ps-1.5 flex items-center w-full min-h-[40px]">
                <Search class="min-w-5" />
                <input
                  ref="inputRef"
                  type="text"
                  v-model="searchTerm"
                  @focus="isSearchFocused = true"
                  class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
                  placeholder="Search & select your destination..."
                />
              </div>
              <div v-if="displayedSearchResults.length > 0 || isSearching" class="w-full px-1.5">
                <div class="w-full h-[1px] bg-neu-200"></div>
                <div class="py-4 flex gap-4 flex-col">
                  <div
                    v-for="destination in displayedSearchResults"
                    :key="destination.id"
                    @click="selectDestination(destination)"
                    class="flex items-center cursor-pointer gap-3 px-3 py-1.5 transition duration-300 hover:bg-[#EFF6F2] rounded-2xl"
                  >
                    <img
                      :src="destination.primary_image_url || 'https://placehold.co/60x60'"
                      class="object-cover size-15 rounded-xl"
                    />
                    <div class="flex flex-col gap-1.5">
                      <h3 class="text-sm font-semibold">{{ destination.name }}</h3>
                      <div class="flex gap-1 items-center">
                        <Location class="size-4" />
                        <p class="text-xs font-medium text-neu-600">
                          {{ destination.address.district }}, {{ destination.address.regency }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p class="text-[8px] md:text-[10px] text-neu-50">Photo by tripadvisor</p>
      </div>
    </div>
    <!-- Review Section -->
    <section class="mt-16 md:mt-20 flex flex-col lg:flex-row gap-8 sm:gap-10 lg:gap-16">
      <!-- Left Column -->
      <div class="flex flex-col w-full lg:w-100 xl:w-112">
        <h1
          class="text-4xl sm:text-[42px] font-semibold leading-12 max-w-100 lg:w-full sm:leading-[62px] font-se mb-6"
        >
          Tell us about your
          <span class="text-pr-500">experience</span>
        </h1>
        <div class="flex flex-row lg:flex-col gap-6 lg:gap-12">
          <div
            class="flex flex-col border w-full xs:w-3/4 md:w-1/2 lg:w-full cursor-pointer border-neu-100 rounded-4xl gap-3 p-3"
          >
            <div class="relative w-full">
              <div
                v-if="!selectedDestination"
                class="flex justify-center w-full h-56 lg:h-66 xl:h-74 rounded-3xl font-medium text-xl lg:text-2xl text-center bg-neu-100 items-center p-8"
              >
                First, choose your destination.
              </div>
              <img
                v-else
                :src="selectedDestination.primary_image_url || 'https://placehold.co/400x300'"
                alt="Selected Destination"
                class="object-cover w-full h-74 rounded-3xl"
              />
            </div>
            <div class="flex flex-col">
              <h3 class="text-base sm:text-lg font-semibold">
                {{ selectedDestination?.name || 'Title' }}
              </h3>
              <div
                v-if="selectedDestination?.address"
                class="gap-1 font-medium items-center text-sm sm:text-base mt-1 flex"
              >
                <Location class="size-4 sm:size-5" />{{
                  selectedDestination.address.district || 'District'
                }},
                {{ selectedDestination.address.regency || 'Regency' }}
              </div>
              <p class="text-neu-600 mt-3 text-sm sm:text-base line-clamp-2">
                {{ selectedDestination?.description || 'Descriptions' }}
              </p>
            </div>
          </div>
          <div class="text-center hidden lg:block">
            <p class="text-base md:text-lg font-semibold mb-1">Can’t find the place?</p>
            <p class="text-sm sm:text-base">Tell us about it so we can improve what we show.</p>
            <button
              @click="router.push({ name: 'SuggestSpot' })"
              class="mt-3 px-6 py-2 text-sm sm:text-base font-medium cursor-pointer border border-neu-900 rounded-full"
            >
              Suggest a Spot
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <form @submit.prevent="handleSubmit" class="flex-1 flex-col flex gap-8">
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold"
            >Rate Your Experience</label
          >
          <div class="flex gap-2">
            <button
              v-for="i in 5"
              :key="i"
              @click="setRating(i)"
              @mouseover="hoverRating = i"
              @mouseleave="hoverRating = 0"
              class="transition cursor-pointer"
            >
              <component
                :is="i <= (hoverRating || reviewData.rating) ? StarFilled : Star"
                class="size-7 lg:size-9"
                :class="i <= (hoverRating || reviewData.rating) ? '' : 'text-[#FDB528]'"
              />
            </button>
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="comment" class="text-base md:text-lg font-semibold"
            >Describe the Vibe in Your Words</label
          >
          <textarea
            id="comment"
            rows="7"
            v-model="reviewData.comment"
            :disabled="!selectedDestination"
            placeholder="Clean, quiet, and perfect for relaxing. Highly recommended!"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
          ></textarea>
        </div>

        <div class="flex flex-col">
          <label for="name" class="mb-1 text-base md:text-lg font-semibold"
            >Capture the Moment? Share It!</label
          >
          <p class="text-neu-600 mb-3">Optional</p>
          <div class="w-full">
            <label
              for="photo-upload"
              class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition"
            >
              <Photo class="mb-1" />

              <!-- Text -->
              <p class="text-pr-500 font-medium text-sm mb-[2px]">Click to add photos</p>
              <p class="text-neu-900 text-sm">or drag & drop</p>

              <!-- Hidden input -->
              <input
                id="photo-upload"
                type="file"
                class="hidden"
                multiple
                @change="handleImageUpload"
                :disabled="isUploading"
                accept="image/*"
              />
            </label>
          </div>
          <div v-if="tempImages.length > 0" class="mt-4 grid grid-cols-4 gap-4">
            <div v-for="image in tempImages" :key="image.id" class="relative group aspect-square">
              <img
                :src="image.image"
                :alt="`review-image-${image.id}`"
                class="w-full h-full object-cover rounded-lg"
              />
              <button
                @click="removeTempImage(image)"
                type="button"
                class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100"
              >
                &times;
              </button>
            </div>
          </div>
        </div>

        <label class="flex items-center gap-3">
          <input type="checkbox" class="size-5" required />
          I agree that my review is honest and respectful.
        </label>

        <button
          type="submit"
          :disabled="!selectedDestination"
          class="text-neu-50 px-6 text-base sm:text-lg py-4 font-medium rounded-full"
          :class="{
            'bg-pr-200': !selectedDestination,
            'bg-pr-500 hover:bg-pr-300': selectedDestination,
          }"
        >
          Post My Review
        </button>

        <div class="text-center block lg:hidden mt-12">
          <p class="text-base md:text-lg font-semibold mb-1">Can’t find the place?</p>
          <p class="text-sm sm:text-base">Tell us about it so we can improve what we show.</p>
          <button
            class="mt-3 px-6 py-2 text-sm sm:text-base font-medium border border-neu-900 rounded-full"
          >
            Suggest a Spot
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

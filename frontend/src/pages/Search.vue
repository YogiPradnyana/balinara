<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDestinationStore } from '@/stores/destinationStore'
import { useCategoryStore } from '@/stores/categoryStore' // Asumsi store kategori ada di common
// import { useFacilityStore } from '@/stores/facilityStore'; // Jika Anda punya filter fasilitas

// Import ikon Anda
import Filter from '@/components/icons/Filter.vue'
import Heart from '@/components/icons/Heart.vue'
import Location from '@/components/icons/Location.vue'
import Star from '@/components/icons/Star.vue'
import StarFilled from '@/components/icons/StarFilled.vue'

const route = useRoute()
const router = useRouter()

const destinationStore = useDestinationStore()
const categoryStore = useCategoryStore()
// const facilityStore = useFacilityStore();

// State untuk parameter query, diinisialisasi dari URL
const queryParams = ref({
  page: parseInt(route.query.page) || 1,
  q: route.query.q || '', // 'q' untuk search term, atau 'search' jika itu parameter API Anda
  category: route.query.category || [], // Array untuk multiple categories, akan di-join jadi string saat API call
  regency: route.query.regency || [], // Array untuk multiple regencies
  rating: parseInt(route.query.rating) || 0, // Untuk filter rating
  ordering: route.query.ordering || '-average_rating,name', // Default ordering
})

const ITEMS_PER_PAGE = 10 // Sesuaikan dengan backend

// Computed properties dari store
const destinations = computed(() => destinationStore.allDestinations)
const pagination = computed(() => destinationStore.pagination)
const isLoading = computed(() => destinationStore.isLoadingList)
const DBERROR = computed(() => destinationStore.error)

// Data untuk filter dropdown/checkbox
const categoriesForFilter = computed(() => categoryStore.allCategories)
// const facilitiesForFilter = computed(() => facilityStore.allFacilities);
const allRegencies = ref([
  // Anda bisa fetch ini dari API jika dinamis
  { name: 'Denpasar', slug: 'denpasar' },
  { name: 'Badung', slug: 'badung' },
  { name: 'Gianyar', slug: 'gianyar' },
  { name: 'Tabanan', slug: 'tabanan' },
  { name: 'Klungkung', slug: 'klungkung' },
  { name: 'Bangli', slug: 'bangli' },
  { name: 'Karangasem', slug: 'karangasem' },
  { name: 'Buleleng', slug: 'buleleng' },
  { name: 'Jembrana', slug: 'jembrana' },
])

// State untuk UI filter
const hoverRating = ref(0) // Untuk efek hover pada bintang rating filter
const isFilterOpen = ref(false) // Untuk toggle filter di mobile

// Fungsi untuk mengambil data destinasi
const fetchDestinationsWithParams = () => {
  const paramsToSend = { page: queryParams.value.page, ordering: queryParams.value.ordering }
  if (queryParams.value.q) paramsToSend.search = queryParams.value.q // Ganti 'search' jika parameter API Anda 'q'
  if (queryParams.value.category.length > 0) {
    // Backend DRF DjangoFilterBackend dengan filter 'category__slug' dan lookup 'in' bisa menerima ?category__slug__in=slug1,slug2
    // Atau jika backend Anda menerima multiple params: ?category__slug=slug1&category__slug=slug2
    // Untuk contoh ini, kita kirim comma-separated string. Sesuaikan dengan backend Anda.
    paramsToSend.category_slug = queryParams.value.category.join(',') // Asumsi backend bisa handle comma-separated slugs untuk category
  }
  if (queryParams.value.regency.length > 0) {
    paramsToSend.address_regency = queryParams.value.regency.join(',') // Asumsi filter backend: address__regency__in (atau icontains jika teks)
  }
  if (queryParams.value.rating > 0) {
    paramsToSend.min_rating = queryParams.value.rating
  }

  // Update URL browser dengan query params saat ini
  router.push({ query: paramsToSend }) // Ini akan memicu watcher di bawah jika query berubah
  destinationStore.fetchDestinations(paramsToSend)
}

onMounted(() => {
  // queryParams sudah diinisialisasi dari route.query, jadi langsung fetch
  fetchDestinationsWithParams()

  if (categoriesForFilter.value.length === 0) categoryStore.fetchCategories()
  // if (facilitiesForFilter.value.length === 0) facilityStore.fetchFacilities();
})

// Watcher untuk perubahan filter/search/ordering untuk memicu fetch ulang
// Kita akan watch objek queryParams secara keseluruhan, tapi exclude 'page' dari trigger reset page
watch(
  () => ({ ...queryParams.value, page: undefined }),
  (newParams, oldParams) => {
    // Hanya fetch jika ada perubahan signifikan selain 'page'
    // Perbandingan objek bisa tricky, cara sederhana: serialize ke string
    if (JSON.stringify(newParams) !== JSON.stringify(oldParams)) {
      queryParams.value.page = 1 // Selalu reset ke halaman 1 saat filter/search/ordering berubah
      fetchDestinationsWithParams()
    }
  },
  { deep: true },
)

// Fungsi untuk Paginasi
const goToPage = (page) => {
  const totalPages = Math.ceil(pagination.value.count / ITEMS_PER_PAGE) || 1
  if (page > 0 && page <= totalPages) {
    queryParams.value.page = page
    fetchDestinationsWithParams() // URL akan diupdate oleh fetchDestinationsWithParams
  }
}

const viewDestinationDetail = (slug) => {
  router.push({ name: 'DetailDestination', params: { slug: slug } })
}

// Handler untuk filter
const toggleFilterSelection = (type, value) => {
  if (!queryParams.value[type]) {
    queryParams.value[type] = []
  }
  const selectedArray = queryParams.value[type]
  const index = selectedArray.indexOf(value)
  if (index > -1) {
    selectedArray.splice(index, 1)
  } else {
    if (type === 'regency') {
      // Jika regency radio button (hanya satu pilihan)
      queryParams.value[type] = [value]
    } else {
      // Jika category checkbox (bisa banyak pilihan)
      selectedArray.push(value)
    }
  }
  // Watcher di atas akan otomatis memicu fetch ulang
}

const setSelectedRating = (rating) => {
  queryParams.value.rating = queryParams.value.rating === rating ? 0 : rating // Klik lagi untuk clear
  // Watcher akan memicu fetch
}

// Untuk keyword, kita ambil dari queryParams.q yang di-v-model ke input
const keyword = computed({
  get: () => queryParams.value.q,
  set: (value) => {
    queryParams.value.q = value
  }, // Watcher akan handle debounce dan fetch
})
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] bg-[#ECF4F0] pb-24 md:pb-30">
    <div class="flex flex-col md:flex-row gap-8 pt-10 md:pt-16">
      <!-- Sidebar -->
      <div class="min-w-52 lg:min-w-60 space-y-5 lg:space-y-8 hidden md:block">
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Categories</h3>
          <ul class="space-y-1.5">
            <li v-for="cat in categoriesForFilter" :key="cat.slug">
              <label class="flex items-center gap-2">
                <input
                  type="checkbox"
                  :value="cat.slug"
                  :checked="queryParams.category.includes(cat.slug)"
                  @change="toggleFilterSelection('category', cat.slug)"
                />{{ cat.name }}
              </label>
            </li>
          </ul>
        </div>
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Regency</h3>
          <ul class="space-y-1.5">
            <li v-for="reg in allRegencies" :key="reg.slug">
              <label class="flex items-center gap-2">
                <input
                  type="radio"
                  :value="reg.slug"
                  :checked="queryParams.regency.includes(reg.slug)"
                  @change="toggleFilterSelection('regency', reg.slug)"
                />
                {{ reg.name }}
              </label>
            </li>
          </ul>
        </div>
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Rating</h3>
          <div class="flex gap-1">
            <button
              v-for="i in 5"
              :key="i"
              @click="setSelectedRating(i)"
              @mouseover="hoverRating = i"
              @mouseleave="hoverRating = 0"
              class="text-2xl transition"
              :aria-label="`Set rating to ${i}`"
              :class="{
                'opacity-50': queryParams.rating > 0 && queryParams.rating !== i && !hoverRating,
              }"
            >
              <component
                :is="i <= (hoverRating || queryParams.rating) ? StarFilled : Star"
                class="size-6 lg:size-8"
                :class="i <= (hoverRating || queryParams.rating) ? '' : 'text-[#FDB528]'"
              />
            </button>
          </div>
          <button
            v-if="queryParams.rating > 0"
            @click="setSelectedRating(0)"
            class="mt-2 text-xs text-pr-500 hover:underline"
          >
            Clear Rating
          </button>
        </div>
      </div>

      <!-- Search Result List -->
      <div class="flex-1 flex flex-col">
        <h1 class="text-2xl md:mb-1 md:text-[32px] font-se font-semibold leading-10 md:leading-12">
          Search results for "{{ keyword || 'All Destinations' }}"
        </h1>
        <p class="text-sm sm:text-base">
          Your adventure starts with places we found for you.
          <span v-if="pagination.count > 0"> ({{ pagination.count }} results)</span>
        </p>
        <div class="md:hidden flex relative w-full justify-end">
          <button
            @click="isFilterOpen = !isFilterOpen"
            class="flex w-fit rounded-lg mt-2 bg-sur-50 p-2 items-center justify-center"
            aria-expanded="isFilterOpen"
            aria-controls="mobile-filters"
          >
            <Filter class="size-5" />
          </button>
          <div
            v-if="isFilterOpen"
            id="mobile-filters"
            class="md:hidden top-13 min-w-56 p-4 absolute bg-sur-50 shadow-sm rounded-2xl flex flex-col gap-4"
          >
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Categories</h3>
              <ul class="space-y-1.5 text-sm">
                <li v-for="cat in categoriesForFilter" :key="cat.slug + '-mobile'">
                  <label class="flex items-center gap-1.5 cursor-pointer">
                    <input
                      type="checkbox"
                      :value="cat.slug"
                      :checked="queryParams.category.includes(cat.slug)"
                      @change="toggleFilterSelection('category', cat.slug)"
                    />
                    {{ cat.name }}
                  </label>
                </li>
              </ul>
            </div>
            <div class="w-3/4 h-[1px] bg-neu-100"></div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Regency</h3>
              <ul class="space-y-1.5 text-sm">
                <li v-for="reg in allRegencies" :key="reg.slug + '-mobile'">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      :value="reg.slug"
                      :checked="queryParams.regency.includes(reg.slug)"
                      @change="toggleFilterSelection('regency', reg.slug)"
                    />
                    {{ reg.name }}
                  </label>
                </li>
              </ul>
            </div>
            <div class="w-3/4 h-[1px] bg-neu-100"></div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Rating</h3>
              <div class="flex gap-1">
                <button
                  v-for="i in 5"
                  :key="i + '-mobile-star'"
                  @click="setSelectedRating(i)"
                  @mouseover="hoverRating = i"
                  @mouseleave="hoverRating = 0"
                  class="text-2xl transition"
                >
                  <component
                    :is="i <= (hoverRating || selectedRating) ? StarFilled : Star"
                    class="size-5"
                    :class="i <= (hoverRating || selectedRating) ? '' : 'text-[#FDB528]'"
                  />
                </button>
              </div>
              <button
                v-if="queryParams.rating > 0"
                @click="setSelectedRating(0)"
                class="mt-2 text-xs ..."
              >
                Clear Rating
              </button>
              <button
                @click="isFilterOpen = false"
                class="mt-4 w-full py-2 bg-pr-500 text-white rounded-lg"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
        <div v-if="isLoading && destinations.length === 0" class="text-center py-10">
          <p class="text-gray-500 dark:text-gray-400">Finding amazing places for you...</p>
        </div>
        <div
          v-else-if="DBERROR && destinations.length === 0 && !isLoading"
          class="my-6 p-4 bg-red-100 text-red-700 rounded-lg"
        >
          <p>Oops! {{ DBERROR }}</p>
        </div>
        <!-- Card -->
        <ul
          v-else-if="!isLoading && destinations.length > 0"
          class="flex gap-4 mt-4 md:mt-6 flex-col"
        >
          <div
            v-for="destination in destinations"
            :key="destination.slug"
            @click="viewDestinationDetail(destination.slug)"
            class="flex bg-sur-50 rounded-4xl p-4 gap-3 sm:gap-5 items-center w-full"
          >
            <div
              class="relative overflow-hidden size-32 xs:size-36 md:size-40 lg:size-45 rounded-3xl"
            >
              <img
                :src="destination.primary_image_url || 'https://placehold.co/160x160'"
                :alt="destination.name"
                class="object-cover w-full h-full"
              />
              <div
                class="flex flex-col justify-between items-end absolute bottom-0 top-0 left-0 right-0 p-3"
              >
                <div class="p-2 flex items-center justify-center bg-sur-50 rounded-full w-fit">
                  <Heart class="size-6 text-neu-900" />
                </div>
                <p class="text-[8px] w-full text-start md:text-[10px] text-neu-50">
                  Photo by unsplash
                </p>
              </div>
            </div>

            <div class="flex flex-col flex-1">
              <div class="flex justify-between">
                <div>
                  <h3 class="font-semibold text-base md:text-lg line-clamp-1">
                    {{ destination.name }}
                  </h3>
                  <div class="gap-1 md:mt-1 font-medium text-xs md:text-sm items-center flex">
                    <Location class="size-4 md:size-4.5" /><span class="line-clamp-1">{{
                      destination.address_brief
                    }}</span>
                  </div>
                </div>
                <div
                  v-if="destination.average_rating > 0"
                  class="py-1 px-2 sm:px-2.5 flex items-center border border-neu-200 justify-center w-fit h-fit font-medium text-xs sm:text-sm gap-1 bg-sur-50 rounded-full"
                >
                  <StarFilled class="size-4 md:size-4.5" />
                  {{ parseFloat(destination.average_rating).toFixed(1) }}
                </div>
              </div>

              <p class="text-sm md:text-base text-neu-600 mt-2 lg:mt-3 line-clamp-2">
                {{ destination.description || 'Discover the beauty of this destination.' }}
              </p>

              <button
                type="button"
                @click.stop="viewDestinationDetail(destination.slug)"
                class="px-6 py-2 mt-3 sm:mt-4 lg:mt-6 flex gap-2 w-fit cursor-pointer items-center justify-center text-xs md:text-sm font-medium bg-pr-500 rounded-full text-neu-50"
              >
                View More
              </button>
            </div>
          </div>
        </ul>
        <div
          v-else-if="!isLoading && destinations.length === 0 && !DBERROR"
          class="text-center py-10 text-gray-500 dark:text-gray-400"
        >
          No destinations found matching your criteria.
        </div>

        <!-- Paginasi -->
        <div
          v-if="!isLoading && pagination.count > ITEMS_PER_PAGE"
          class="mt-8 flex justify-center items-center space-x-1 sm:space-x-2"
        >
          <button
            @click="goToPage(queryParams.page - 1)"
            :disabled="!pagination.previous"
            class="px-3 py-1.5 sm:px-4 sm:py-2 border rounded-md disabled:opacity-50 text-sm ..."
          >
            Prev
          </button>
          <!-- Anda bisa loop untuk nomor halaman di sini -->
          <span class="text-sm text-gray-700 dark:text-gray-300"
            >Page {{ queryParams.page }} of
            {{ Math.ceil(pagination.count / ITEMS_PER_PAGE) || 1 }}</span
          >
          <button
            @click="goToPage(queryParams.page + 1)"
            :disabled="!pagination.next"
            class="px-3 py-1.5 sm:px-4 sm:py-2 border rounded-md disabled:opacity-50 text-sm ..."
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

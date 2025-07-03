<script setup>
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
import { ref, onMounted, computed, watch, h } from 'vue'
import { useDestinationStore } from '@/stores/destinationStore'
import ConfirmationToast from '@/components/ConfirmationToast.vue'
import {
  showNotification,
  showConfirmationToast,
  dismissCurrentConfirmationToast,
} from '@/services/notificationService'
import ToggleSwitch from '@/components/ToggleSwitch.vue'

const queryParams = ref({
  page: 1,
  search: '',
})

const destinationStore = useDestinationStore()
const destinations = computed(() => destinationStore.destinations)
const pagination = computed(() => destinationStore.pagination)
const isLoading = computed(() => destinationStore.isLoadingList)

const fetchDestinationsWithParams = () => {
  destinationStore.fetchDestinations(queryParams.value)
}

onMounted(() => {
  fetchDestinationsWithParams()
})

const ITEMS_PER_PAGE = 10

// Hitung nomor item awal dan akhir untuk tampilan "Showing X to Y of Z Entries"
const firstItemNumber = computed(() => {
  if (pagination.value.count === 0) return 0
  return (queryParams.value.page - 1) * ITEMS_PER_PAGE + 1
})
const lastItemNumber = computed(() => {
  const last = queryParams.value.page * ITEMS_PER_PAGE
  return Math.min(last, pagination.value.count)
})
let searchTimeout = null
watch(
  () => queryParams.value.search,
  (newSearchTerm) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      queryParams.value.page = 1 // Reset ke halaman 1 saat search baru
      fetchDestinationsWithParams()
    }, 500) // Debounce 500ms
  },
)

// Fungsi Delete tetap di sini karena aksinya ada di halaman ini
const confirmDelete = (destination) => {
  const message = `Are you sure you want to move "${destination.name}" to the Trash?`
  const onConfirm = async () => {
    try {
      await destinationStore.deleteDestination(destination.slug)
      showNotification('success', 'Destination deleted successfully')
      if (destinations.value.length === 1 && queryParams.value.page > 1) {
        queryParams.value.page--
      }
      fetchDestinationsWithParams()
    } catch (error) {
      showNotification('error', destinationStore.error || 'Failed to delete destination.')
    }
    dismissCurrentConfirmationToast()
  }
  showConfirmationToast(
    h(ConfirmationToast, { message, onConfirm, onCancel: dismissCurrentConfirmationToast }),
  )
}

async function handleTogglePublish(slug, currentState) {
  const message = `Are you sure you want to change the status of this destination to "${currentState ? 'Draft' : 'Published'}"?`
  const onConfirm = async () => {
    try {
      await destinationStore.togglePublish(slug)
      showNotification('success', 'Status changed successfully')
    } catch (error) {
      showNotification('error', destinationStore.error || 'Failed to change status')
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

function formatAddress(address) {
  if (!address) {
    return 'N/A'
  }
  // Menggabungkan bagian alamat menjadi satu string yang rapi
  const parts = [address.sub_district, address.district, address.regency]
  return parts.filter((part) => part).join(', ') // filter(part => part) untuk menghapus bagian yang kosong
}

// Fungsi untuk navigasi halaman
const goToPage = (pageNumber) => {
  if (pageNumber < 1) return
  // Cek apakah halaman berikutnya ada berdasarkan pagination.next atau hitungan
  const totalPages = Math.ceil(pagination.value.count / ITEMS_PER_PAGE)
  if (pageNumber > totalPages && pagination.value.count > 0) return // Jangan melebihi total halaman

  queryParams.value.page = pageNumber
  fetchCategoriesWithParams()
}

const goToNextPage = () => {
  if (pagination.value.next) {
    // Gunakan URL next dari API jika ada
    // Anda perlu parsing nomor halaman dari URL pagination.value.next
    // atau cukup increment queryParams.value.page dan biarkan goToPage yang validasi
    goToPage(queryParams.value.page + 1)
  }
}

const goToPrevPage = () => {
  if (pagination.value.previous) {
    // Gunakan URL previous dari API jika ada
    goToPage(queryParams.value.page - 1)
  }
}
</script>
<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Destinations</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Destinations</span>
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
              placeholder="Search something..."
            />
          </div>
          <RouterLink
            :to="{ name: 'AdminDestinationCreate' }"
            class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
          >
            <Plus class="size-5" />
            New Destination
          </RouterLink>
        </div>

        <!-- Indikator Loading -->
        <div v-if="isLoading && destinations.length === 0" class="text-center py-8">
          <p class="text-gray-500 dark:text-gray-400">Loading destinations...</p>
          <!-- Anda bisa menambahkan spinner di sini -->
        </div>

        <!-- Pesan Error -->
        <div
          v-if="destinationStore.error && destinations.length === 0"
          class="mb-4 p-3 bg-red-100 text-red-700 rounded-md"
        >
          <p>Error: {{ destinationStore.error }}</p>
        </div>

        <div
          v-if="!isLoading && destinations.length > 0"
          class="mt-4 overflow-hidden border border-neu-100 rounded-2xl"
        >
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">NAME</th>
                  <th class="p-4 text-start font-semibold">STATUS</th>
                  <th colspan="2" class="p-4 text-start font-semibold">ADDRESS</th>
                  <th class="p-4 text-start font-semibold">PHONE NUMBER</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(destination, index) in destinations"
                  :key="destination.id"
                  class="text-sm text-neu-700 border-b border-neu-100"
                >
                  {{
                    destination.address_brief
                  }}
                  <td class="p-4 text-neu-900">{{ calculateItemNumber(index) }}</td>
                  <td class="p-4 text-neu-900 font-semibold">{{ destination.name }}</td>
                  <td class="p-4 font-medium flex items-center gap-2">
                    <ToggleSwitch
                      :is-active="destination.is_published"
                      @toggle="handleTogglePublish(destination.slug, destination.is_published)"
                    />
                    <span :class="destination.is_published ? 'text-green-600' : 'text-neu-500'">
                      {{ destination.is_published ? 'Published' : 'Draft' }}
                    </span>
                  </td>
                  <td colspan="2" class="p-4">{{ formatAddress(destination.address) }}</td>
                  <td class="p-4">{{ destination.contact?.phone }}</td>
                  <td class="p-4 flex gap-3">
                    <RouterLink
                      :to="{ name: 'AdminDestinationEdit', params: { slug: destination.slug } }"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#F0BF05] bg-[#FACA15]"
                    >
                      <Edit class="size-5 text-neu-900" />
                    </RouterLink>
                    <RouterLink
                      :to="{ name: 'AdminDestinationDetail', params: { slug: destination.slug } }"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </RouterLink>
                    <button
                      type="button"
                      @click="confirmDelete(destination)"
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
        <div
          v-if="!isLoading && destinations.length === 0 && !destinationStore.error"
          class="text-center py-8 text-gray-500 dark:text-gray-400"
        >
          No destinations found. Try a different search or add a new one!
        </div>

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

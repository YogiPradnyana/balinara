<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSuggestionStore } from '@/stores/suggestionStore'
import { RouterLink } from 'vue-router'
import { debounce } from 'lodash-es'
// showNotification dan ConfirmationToast tidak lagi diperlukan jika tombol hapus dihilangkan
// import { showNotification } from '@/services/notificationService' 
// import ConfirmationToast from '@/components/ConfirmationToast.vue' 

// Impor ikon Anda
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Show from '@/components/icons/Show.vue'
// TrashCan tidak lagi diperlukan karena tombol hapus dihilangkan
// import TrashCan from '@/components/icons/TrashCan.vue' 
import Search from '@/components/icons/Search.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'

const suggestionStore = useSuggestionStore()

const tabs = ref([
  { id: 'all', label: 'All', value: '' },
  { id: 'pending', label: 'Pending', value: 'pending' },
  { id: 'approved', label: 'Approved', value: 'approved' },
  { id: 'rejected', label: 'Rejected', value: 'rejected' },
])

const activeTab = ref('all') // Ubah default tab menjadi 'all'
const searchQuery = ref('')
const currentPage = ref(1)

const suggestions = computed(() => suggestionStore.adminSuggestions)
const pagination = computed(() => suggestionStore.pagination)

const currentParams = computed(() => {
    const params = { page: currentPage.value, search: searchQuery.value }
    const activeTabObject = tabs.value.find(t => t.id === activeTab.value)
    
    if (activeTabObject && activeTabObject.value) {
        params.status = activeTabObject.value
    }
    return params
})

const loadSuggestions = () => {
  console.log("Loading suggestions with params:", currentParams.value);
  suggestionStore.fetchAdminSuggestions(currentParams.value)
  // Pastikan Anda memanggil action untuk hitungan sidebar di sini atau di App.vue/layout admin
  // Jika tidak, angka di sidebar tidak akan update saat filter diubah di halaman ini.
  suggestionStore.fetchAllSuggestionsForAdminCount(); 
}

onMounted(loadSuggestions)

watch(activeTab, () => {
  currentPage.value = 1
  loadSuggestions()
})

watch(searchQuery, debounce(() => {
    currentPage.value = 1
    loadSuggestions()
}, 500))

const setActiveTab = (tabId) => {
  activeTab.value = tabId
}

const changePage = (direction) => {
    if (direction === 'next' && pagination.value.next) {
        currentPage.value++;
    } else if (direction === 'prev' && pagination.value.previous) {
        currentPage.value--;
    }
    loadSuggestions();
}

// Fungsi handleDelete dihilangkan karena tombol hapus tidak ada lagi
// const handleDelete = async (id, name) => {
//     showNotification({
//       component: ConfirmationToast,
//       props: {
//         message: `Apakah Anda yakin ingin menghapus saran untuk "${name}"?`,
//         onConfirm: async () => {
//           try {
//             await suggestionStore.deleteSuggestion(id, currentParams.value);
//             showNotification('success', `Saran "${name}" berhasil dihapus.`);
//           } catch (error) {
//             showNotification('error', `Gagal menghapus saran "${name}".`);
//             console.error('Delete error:', error);
//           }
//         },
//         onCancel: () => {
//           showNotification('info', `Penghapusan saran "${name}" dibatalkan.`);
//         },
//       },
//       duration: 0, 
//     });
// }
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Suggested Spot</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Suggested Spot</span>
      </div>
    </div>

    <div class="flex flex-col rounded-3xl border border-neu-100 p-4">
      <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
        <div class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full">
          <Search class="size-6" />
          <input
            v-model="searchQuery"
            type="text"
            class="w-full text-xs md:text-sm focus:outline-none"
            placeholder="Cari nama tempat, traveler, atau alamat..."
          />
        </div>
      </div>

      <div class="mt-4">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-4 overflow-x-auto" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="setActiveTab(tab.id)"
              :class="[
                activeTab === tab.id
                  ? 'border-pr-500 text-pr-600'
                  : 'border-transparent text-neu-500 hover:text-neu-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <div class="mt-4 overflow-hidden">
            <div v-if="suggestionStore.isLoading" class="text-center p-8">Memuat data...</div>
            <div v-else-if="suggestionStore.error" class="text-center p-8 text-red-500">Gagal memuat data.</div>
            <div v-else-if="!suggestions || suggestions.length === 0" class="text-center p-8 text-gray-500">Tidak ada data untuk ditampilkan.</div>
            <div v-else class="max-w-full overflow-x-auto">
              <table class="min-w-full w-full">
                <thead class="bg-pr-500 text-xs text-white">
                  <tr>
                    <th class="p-4 text-start font-semibold">NO</th>
                    <th class="p-4 text-start font-semibold">NAME</th>
                    <th class="p-4 text-start font-semibold">TRAVELER NAME</th>
                    <th class="p-4 text-start font-semibold">CATEGORY</th>
                    <th class="p-4 text-start font-semibold">ADDRESS</th>
                    <th class="p-4 text-start font-semibold">ACTION</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(suggestion, index) in suggestions" :key="suggestion.id" class="text-sm text-neu-700 border-b border-neu-100">
                    <td class="p-4 text-neu-900">{{ (currentPage - 1) * 10 + index + 1 }}</td>
                    <td class="p-4 text-neu-900 font-semibold">{{ suggestion.name }}</td>
                    <td class="p-4">{{ suggestion.suggester_username }}</td>
                    <td class="p-4">
                      <span v-if="suggestion.categories_details && suggestion.categories_details.length > 0">
                        {{ suggestion.categories_details.map(c => c.name).join(', ') }}
                      </span>
                      <span v-else>-</span>
                    </td>
                    <td class="p-4">{{ suggestion.regency }}</td>
                    <td class="p-4 flex gap-3">
                      <RouterLink
                        :to="{ name: 'AdminSuggestionDetail', params: { id: suggestion.id } }"
                        class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                      >
                        <Show class="size-5 text-neu-50" />
                      </RouterLink>
                      </td>
                  </tr>
                </tbody>
              </table>
            </div>
        </div>
        
        <div v-if="!suggestionStore.isLoading && suggestions && suggestions.length > 0" class="flex justify-between items-center gap-3 flex-wrap mt-3">
            <div class="text-sm text-neu-600">
                Menampilkan <span class="font-medium text-neu-900">{{ (currentPage - 1) * 10 + 1 }}</span> sampai
                <span class="font-medium text-neu-900">{{ Math.min(currentPage * 10, pagination.count) }}</span> dari
                <span class="font-medium text-neu-900">{{ pagination.count }}</span> Entri
            </div>
            <div class="flex items-center rounded-[8px] overflow-hidden">
                <button @click="changePage('prev')" :disabled="!pagination.previous" class="flex bg-neu-100 text-neu-700 disabled:text-neu-300 gap-2 h-8 px-3 items-center font-semibold">
                    <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
                </button>
                <button @click="changePage('next')" :disabled="!pagination.next" class="flex bg-neu-100 text-neu-700 disabled:text-neu-300 gap-2 h-8 px-3 items-center font-semibold">
                    Next<ArrowRight2Bold class="size-4" />
                </button>
            </div>
        </div>

      </div>
    </div>
    </div>
</template>
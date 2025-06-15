<script setup>
import { ref, watch, onMounted, computed, h } from 'vue'
import { useCategoryStore } from '@/stores/categoryStore'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
import CategoryFormModal from './CategoryFormModal.vue'
import { toast } from 'vue-sonner'
import ConfirmationToast from '@/components/ConfirmationToast.vue'
import {
  showNotification,
  showConfirmationToast,
  dismissCurrentConfirmationToast,
} from '@/services/notificationService'

const showFormModal = ref(false)
const categoryToEdit = ref(null)

const categoryStore = useCategoryStore()

const categories = computed(() => categoryStore.allCategories)
const pagination = computed(() => categoryStore.pagination)

// State lokal untuk parameter query API (termasuk halaman saat ini)
const queryParams = ref({
  page: 1,
  search: '',
  // Tambahkan parameter filter lain jika ada (misalnya, ordering)
})

// Ukuran halaman, harus sesuai dengan PAGE_SIZE di backend atau dikirim sebagai parameter
const ITEMS_PER_PAGE = 10 // Sesuaikan dengan PAGE_SIZE Django Anda

// Hitung nomor item awal dan akhir untuk tampilan "Showing X to Y of Z Entries"
const firstItemNumber = computed(() => {
  if (pagination.value.count === 0) return 0
  return (queryParams.value.page - 1) * ITEMS_PER_PAGE + 1
})
const lastItemNumber = computed(() => {
  const last = queryParams.value.page * ITEMS_PER_PAGE
  return Math.min(last, pagination.value.count)
})

const fetchCategoriesWithParams = () => {
  categoryStore.fetchCategories(queryParams.value)
}

onMounted(() => {
  fetchCategoriesWithParams()
})

// Watch perubahan pada queryParams.search untuk melakukan pencarian (dengan debounce jika mau)
let searchTimeout = null
watch(
  () => queryParams.value.search,
  (newSearchTerm) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      queryParams.value.page = 1 // Reset ke halaman 1 saat search baru
      fetchCategoriesWithParams()
    }, 500) // Debounce 500ms
  },
)

watch(showFormModal, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const openCreateModal = () => {
  categoryToEdit.value = null // Mode create
  categoryStore.clearError() // Bersihkan error sebelumnya jika ada
  showFormModal.value = true
}

const openEditModal = (category) => {
  categoryToEdit.value = { ...category } // Kirim salinan agar tidak langsung mengubah state
  categoryStore.clearError()
  showFormModal.value = true
}

const closeFormModal = () => {
  showFormModal.value = false
  categoryToEdit.value = null
}

const handleSaveCategory = async (formData) => {
  try {
    if (formData.slug) {
      // Jika ada slug, berarti update
      await categoryStore.updateCategory(formData.slug, formData)
      showNotification('success', 'Category updated successfully')
    } else {
      // Jika tidak ada ID, berarti create
      await categoryStore.createCategory(formData)
      showNotification('success', 'Category added successfully')
    }
    closeFormModal()
    // Opsional: panggil fetchCategories lagi jika ingin data benar-benar sinkron,
    // tapi action create/update sudah mencoba update state lokal.
    fetchCategoriesWithParams()
  } catch (error) {
    // Error sudah di-set di store, form modal bisa menampilkannya
    // atau Anda bisa menangani error spesifik di sini jika perlu.
    console.error('Save category failed in page:', error)
    // Biarkan error ditampilkan oleh CategoryFormModal atau getter categoryStore.categoryError
  }
}

// Di dalam confirmDelete di CategoryLists.vue
const confirmDelete = async (category) => {
  const message = `Are you sure you want to delete category "${category.name}"? This cannot be undone.`

  // Fungsi yang akan dijalankan jika user menekan "Ya"
  const handleConfirm = async () => {
    // 'toastId' dari scope luar tidak langsung tersedia di sini
    // kecuali jika Anda menangkapnya dan meneruskannya atau menggunakan cara lain
    // Namun, kita akan dismiss berdasarkan ID yang dibuat oleh showConfirmationToast
    try {
      await categoryStore.deleteCategory(category.slug)
      showNotification('success', 'Category deleted successfully') // Gunakan helper notifikasi
      if (categories.value.length === 0 && queryParams.value.page > 1) {
        queryParams.value.page--
      }
      fetchCategoriesWithParams()
    } catch (error) {
      showNotification('error', categoryStore.categoryError || 'Failed to delete category.')
    }
  }

  // Fungsi yang akan dijalankan jika user menekan "Batal"
  const handleCancel = () => {
    console.log('Penghapusan dibatalkan.')
    // Tidak perlu dismiss di sini jika onCancel di ConfirmationToast sudah melakukannya
  }

  // Menampilkan toast dengan komponen kustom
  // showConfirmationToast akan membuat ID internal dan mengembalikannya
  showConfirmationToast(
    // Simpan ID yang dikembalikan
    h(ConfirmationToast, {
      message,
      onConfirm: () => {
        dismissCurrentConfirmationToast()
        handleConfirm()
      },
      onCancel: () => {
        dismissCurrentConfirmationToast()
        handleCancel()
      },
    }),
  )
}

// Fungsi untuk penomoran baris
const calculateItemNumber = (indexInPage) => {
  return (queryParams.value.page - 1) * ITEMS_PER_PAGE + indexInPage + 1
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
  <CategoryFormModal
    v-if="showFormModal"
    :category-data="categoryToEdit"
    @save="handleSaveCategory"
    @close="showFormModal = false"
  />
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Categories</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Categories</span>
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
          <button
            type="button"
            @click="openCreateModal"
            class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
          >
            <Plus class="size-5" />
            New Category
          </button>
        </div>
        <!-- Indikator Loading -->
        <div
          v-if="categoryStore.isLoadingCategories && categories.length === 0"
          class="text-center py-8"
        >
          <p class="text-gray-500 dark:text-gray-400">Loading categories...</p>
          <!-- Anda bisa menambahkan spinner di sini -->
        </div>

        <!-- Pesan Error -->
        <div
          v-if="categoryStore.categoryError && categories.length === 0"
          class="mb-4 p-3 bg-red-100 text-red-700 rounded-md"
        >
          <p>Error: {{ categoryStore.categoryError }}</p>
        </div>

        <div
          v-if="!categoryStore.isLoadingCategories && categories.length > 0"
          class="mt-4 overflow-hidden border border-neu-100 rounded-2xl"
        >
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">NAME</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(category, index) in categories"
                  :key="category.id"
                  class="text-sm text-neu-700 border-b border-neu-100"
                >
                  <td class="p-4 text-neu-900">{{ calculateItemNumber(index) }}</td>
                  <td class="p-4 text-neu-900 font-semibold">{{ category.name }}</td>
                  <td class="p-4 flex gap-3">
                    <button
                      type="button"
                      @click="openEditModal(category)"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#F0BF05] bg-[#FACA15]"
                    >
                      <Edit class="size-5 text-neu-900" />
                    </button>
                    <button
                      type="button"
                      @click="confirmDelete(category)"
                      aria-label="Delete category"
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
          v-if="
            !categoryStore.isLoadingCategories &&
            categories.length === 0 &&
            !categoryStore.categoryError
          "
          class="text-center py-8 text-gray-500 dark:text-gray-400"
        >
          No categories found. Try a different search or add a new one!
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

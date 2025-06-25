<script setup lang="ts">
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'
import Subtract from '@/components/icons/Subtract.vue'
import { RouterLink } from 'vue-router'
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDestinationStore } from '@/stores/destinationStore'
import DestinationForm from '@/components/admin/destinations/DestinationForm.vue'
import { showNotification } from '@/services/notificationService'

const store = useDestinationStore()
const router = useRouter()
const route = useRoute()
const formErrors = ref(null)

const slug = route.params.slug

const selectedFiles = ref([])
const isUploading = ref(false)
const imageUploadInput = ref(null)

// Ambil data lama saat halaman dimuat
onMounted(() => {
  store.fetchDestinationBySlug(slug)
})

const isLoading = computed(() => store.isLoadingDetail)
const destinationToEdit = computed(() => store.currentDestination)

async function handleUpdateDestination(formData) {
  try {
    await store.updateDestination(slug, formData)
    showNotification('success', 'Destination updated successfully')
    router.push({ name: 'AdminDestinations' })
  } catch (error) {
    formErrors.value = error.response?.data
    console.error('Full error response:', formErrors.value)
  }
}

function onFileChange(event) {
  // event.target.files adalah sebuah FileList, kita ubah menjadi array
  selectedFiles.value = Array.from(event.target.files)
}

// 2. Fungsi untuk meng-upload semua file yang dipilih
async function handleImageUpload() {
  if (selectedFiles.value.length === 0) {
    alert('Please select one or more image files to upload.')
    return
  }
  isUploading.value = true

  // Buat objek FormData untuk mengirim file
  const formData = new FormData()
  // Loop dan tempelkan setiap file dengan nama 'images'
  for (const file of selectedFiles.value) {
    formData.append('images', file, file.name) // 'images' harus cocok dengan .getlist('images') di backend
  }

  try {
    await store.uploadDestinationImage(slug, formData)
    showNotification('success', `${selectedFiles.value.length} image(s) uploaded successfully!`)

    // Reset input file setelah berhasil
    selectedFiles.value = []
    if (imageUploadInput.value) {
      imageUploadInput.value.value = ''
    }
  } catch (error) {
    showNotification('error', 'An error occurred during upload. Some files may have failed.')
  } finally {
    isUploading.value = false
  }
}

// 3. Fungsi untuk menghapus gambar
async function handleImageDelete(imageId) {
  if (confirm('Are you sure you want to delete this image?')) {
    try {
      await store.deleteDestinationImage(slug, imageId)
      showNotification('success', 'Image deleted.')
    } catch (error) {
      showNotification('error', 'Failed to delete image.')
    }
  }
}
</script>

<template>
  <div v-if="isLoading" class="p-8 text-center text-gray-500">Loading Destination...</div>
  <div v-else-if="destinationToEdit" class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Edit Destination</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminDestinations' }" class="hover:underline"
          >Destinations</RouterLink
        >
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Edit</span>
      </div>
    </div>
    <DestinationForm
      v-if="destinationToEdit"
      :is-edit-mode="true"
      :initial-data="destinationToEdit"
      :is-loading="store.isLoadingDetail"
      @submit="handleUpdateDestination"
      :errors="formErrors"
    />
    <div v-else>Loading data...</div>

    <div v-if="destinationToEdit" class="mt-12 pt-8 border-t">
      <h2 class="text-2xl font-bold mb-6">Manage Gallery</h2>

      <div class="p-6 border bg-gray-50 rounded-lg mb-8">
        <label for="imageUploadInput" class="block text-base font-semibold text-gray-800"
          >Upload New Images</label
        >
        <p class="text-sm text-gray-500 mt-1">You can select multiple images at once.</p>

        <input
          type="file"
          ref="imageUploadInput"
          id="imageUploadInput"
          @change="onFileChange"
          multiple
          accept="image/jpeg, image/png, image/webp"
          class="mt-2 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-pr-100 file:text-pr-700 hover:file:bg-pr-200"
        />

        <button
          @click="handleImageUpload"
          :disabled="isUploading || selectedFiles.length === 0"
          class="mt-4 px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg disabled:bg-gray-400 hover:bg-blue-700"
        >
          {{ isUploading ? 'Uploading...' : `Upload ${selectedFiles.length} File(s)` }}
        </button>
      </div>

      <h3 class="text-xl font-semibold mb-4">
        Current Gallery ({{ destinationToEdit.images.length }} images)
      </h3>
      <div
        v-if="destinationToEdit.images.length > 0"
        class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
      >
        <div
          v-for="image in destinationToEdit.images"
          :key="image.id"
          class="relative group aspect-square"
        >
          <img
            :src="image.image_url"
            :alt="image.alt_text"
            class="w-full h-full object-cover rounded-md shadow-md"
          />
          <div
            class="absolute inset-0 bg-opacity-0 group-hover:bg-opacity-60 transition-all flex items-center justify-center"
          >
            <button
              @click="handleImageDelete(image.id)"
              class="opacity-0 group-hover:opacity-100 px-3 py-1 bg-red-600 text-white text-xs rounded-full transition-opacity"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <p v-else class="text-sm text-gray-500 italic">No images have been uploaded yet.</p>
    </div>
  </div>
</template>

<script setup>
import Subtract from '@/components/icons/Subtract.vue'
import { ref, watchEffect, watch, computed } from 'vue'
import { useCategoryStore } from '@/stores/categoryStore'
import { useFacilityStore } from '@/stores/facilityStore'
import { useDestinationStore } from '@/stores/destinationStore'
import { showNotification } from '@/services/notificationService'
import Photo from '@/components/icons/Photo.vue'
import Hide from '@/components/icons/Hide.vue'
import Show from '@/components/icons/Show.vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({}),
  },
  isEditMode: {
    type: Boolean,
    default: false,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  errors: { type: Object, default: null },
  isReadOnly: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['submit'])

const store = useDestinationStore()

const minPrice = ref('')
const maxPrice = ref('')

const categoryStore = useCategoryStore()
const facilityStore = useFacilityStore()

const tempImagesForCreate = ref([])
const newlyAddedTempImages = ref([])
const imagesMarkedForDeletion = ref(new Set())
const isUploading = ref(false)
const isDragging = ref(false)
const imageError = ref(null)

const formData = ref({
  name: '',
  description: '',
  ticket_price_range: '',
  is_published: false,
  category_ids: [],
  facility_ids: [],
  address_data: {
    street: '',
    sub_district: '',
    district: '',
    regency: '',
    latitude: null,
    longitude: null,
  },
  contact_data: {
    phone: '',
    mail: '',
  },
})

const galleryImages = computed(() => {
  const existingImages = props.isEditMode ? store.currentDestination?.images || [] : []
  const tempImages = props.isEditMode ? newlyAddedTempImages.value : tempImagesForCreate.value
  return [...existingImages, ...tempImages]
})

if (categoryStore.allCategories.length === 0) categoryStore.fetchCategories()
if (facilityStore.allFacilities.length === 0) facilityStore.fetchFacilities()

// 4. "Pengawas" yang akan mengisi form jika ini adalah mode Edit
watch(
  () => props.initialData,
  (newData) => {
    if (props.isEditMode && newData) {
      // Isi form dengan data yang ada
      formData.value.name = newData.name || ''
      formData.value.description = newData.description || ''
      formData.value.ticket_price_range = newData.ticket_price_range || ''
      formData.value.is_published = newData.is_published || false
      formData.value.address_data = { ...(newData.address || formData.value.address_data) }
      formData.value.contact_data = { ...(newData.contact || formData.value.contact_data) }
      formData.value.category_ids = (newData.categories || []).map((c) => c.id)
      formData.value.facility_ids = (newData.facilities || []).map((f) => f.id)

      const priceString = newData.ticket_price_range || ''
      if (priceString.includes(' - ')) {
        const parts = priceString.split(' - ')
        minPrice.value = parts[0] || ''
        maxPrice.value = parts[1] || ''
      } else {
        minPrice.value = priceString
        maxPrice.value = ''
      }
    }
  },
  { immediate: true, deep: true },
)

const handleDrop = (event) => {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  handleFileChange(files)
}

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files)
  handleFileChange(files)
  event.target.value = '' // Reset input file
}

async function handleFileChange(files) {
  if (files.length === 0) return

  imageError.value = null
  isUploading.value = true

  for (const file of files) {
    try {
      const tempImage = await store.uploadTemporaryImage(file)
      const newImageObject = { id: tempImage.id, image_url: tempImage.image, isTemp: true }
      if (props.isEditMode) {
        newlyAddedTempImages.value.push(newImageObject)
      } else {
        tempImagesForCreate.value.push(newImageObject)
      }
    } catch (error) {
      imageError.value = error.image[0] || 'An unknown error occurred during upload.'
    }
  }

  isUploading.value = false
}

async function handleRemoveTempImage(image) {
  if (!image.isTemp) return
  if (props.isEditMode) {
    newlyAddedTempImages.value = newlyAddedTempImages.value.filter((img) => img.id !== image.id)
  } else {
    tempImagesForCreate.value = tempImagesForCreate.value.filter((img) => img.id !== image.id)
  }
}

function toggleDeletionMark(image) {
  // Fungsi ini hanya relevan untuk gambar yang sudah ada (bukan temporer)
  if (image.isTemp) return

  const imageId = image.id
  if (imagesMarkedForDeletion.value.has(imageId)) {
    // Jika sudah ditandai, batalkan (hapus dari Set)
    imagesMarkedForDeletion.value.delete(imageId)
  } else {
    // Jika belum, tandai untuk dihapus (tambahkan ke Set)
    imagesMarkedForDeletion.value.add(imageId)
  }
}

// Helper function untuk UI
function isMarkedForDeletion(imageId) {
  return imagesMarkedForDeletion.value.has(imageId)
}

async function handleSetPrimary(image) {
  if (!props.isEditMode || image.is_primary || image.isTemp) return
  try {
    await store.setPrimaryImage(props.initialData.slug, image.id)
  } catch (error) {
    // error sudah dihandle di store
  }
}

function submitForm() {
  imageError.value = null

  let payload = { ...formData.value }

  if (props.isEditMode) {
    payload.image_ids = newlyAddedTempImages.value.map((img) => img.id)
    payload.delete_image_ids = Array.from(imagesMarkedForDeletion.value)
  } else {
    payload.image_ids = tempImagesForCreate.value.map((img) => img.id)
    if (payload.image_ids.length < 3) {
      imageError.value = 'Please upload at least 3 images.'
      return
    }
  }

  emit('submit', payload)
}

watch([minPrice, maxPrice], ([newMin, newMax]) => {
  // Membersihkan nilai dari titik atau koma jika ada (untuk perhitungan)
  const cleanMin = newMin.replace(/\D/g, '')
  const cleanMax = newMax.replace(/\D/g, '')

  if (cleanMin && cleanMax) {
    // Jika keduanya diisi, format menjadi "Rp X - Rp Y"
    formData.value.ticket_price_range = `Rp ${cleanMin} - Rp ${cleanMax}`
  } else if (cleanMin) {
    // Jika hanya min yang diisi
    formData.value.ticket_price_range = `Start from Rp ${cleanMin}`
  } else if (cleanMax) {
    // Jika hanya max yang diisi
    formData.value.ticket_price_range = `Up to Rp ${cleanMax}`
  } else {
    // Jika keduanya kosong
    formData.value.ticket_price_range = ''
  }
})
</script>
<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Form Left -->
      <div
        class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Name</label>
          <input
            v-model="formData.name"
            type="text"
            id="name"
            :disabled="isReadOnly"
            placeholder="e.g., Hidden Gem Beach Club"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.name, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.name" class="mt-1 text-xs text-red-500">
            {{ errors?.name[0] }}
          </p>
        </div>
        <label
          for="is_published"
          class="rounded-2xl border p-4 cursor-pointer transition-colors duration-200"
          :class="
            formData.is_published ? 'border-green-300 bg-green-50' : 'border-neu-200 bg-gray-50'
          "
        >
          <div class="flex items-center">
            <input
              v-model="formData.is_published"
              type="checkbox"
              id="is_published"
              class="h-4 w-4 rounded border-gray-300 text-green-600 focus:ring-green-500"
            />

            <div class="ml-3 flex flex-col cursor-pointer">
              <span
                class="text-sm font-bold"
                :class="formData.is_published ? 'text-green-700' : 'text-gray-600'"
              >
                {{ formData.is_published ? 'Published' : 'Draft (Hidden)' }}
              </span>
            </div>

            <div class="ml-auto">
              <Show v-if="formData.is_published" class="h-6 w-6 text-green-600" />
              <Hide v-else class="h-6 w-6 text-neu-500" />
            </div>
          </div>

          <p class="text-xs text-gray-600 mt-2">
            If the status is <strong>Published</strong>, the destination will be immediately visible
            to all users on the website.
          </p>
        </label>

        <div class="flex flex-col gap-3">
          <label for="category" class="text-base font-semibold"
            >Category<span class="text-red-500">*</span>
          </label>
          <div class="flex flex-wrap gap-x-6 gap-y-3">
            <label
              v-for="cat in categoryStore.allCategories"
              :key="cat.id"
              class="flex items-center cursor-pointer"
            >
              <input
                type="checkbox"
                :value="cat.id"
                v-model="formData.category_ids"
                :disabled="isReadOnly"
                class="h-4 w-4 rounded border-gray-300"
              />
              <span class="ml-2 text-sm text-gray-700">{{ cat.name }}</span>
            </label>
          </div>
          <p v-if="errors?.category_ids" class="mt-1 text-xs text-red-500">
            {{ errors.category_ids[0] }}
          </p>
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base font-semibold">Descriptions</label>
          <textarea
            v-model="formData.description"
            id="descriptions"
            rows="7"
            :disabled="isReadOnly"
            placeholder="Tell us what makes this place special..."
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
            :class="{ 'border-red-500': errors?.description, 'bg-[#F2F2F2]': isReadOnly }"
          ></textarea>
          <p v-if="errors?.description" class="mt-1 text-xs text-red-500">
            {{ errors?.description[0] }}
          </p>
        </div>
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Facilities</label>
          <div class="flex flex-wrap gap-x-6 gap-y-3">
            <label
              v-for="fac in facilityStore.allFacilities"
              :key="fac.id"
              class="flex items-center cursor-pointer"
            >
              <input
                type="checkbox"
                :value="fac.id"
                v-model="formData.facility_ids"
                class="h-4 w-4 rounded border-gray-300"
                :disabled="isReadOnly"
              />
              <span class="ml-2 text-sm text-neu-900">{{ fac.name }}</span>
            </label>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Entrance Ticket</label>
          <div class="flex gap-2.5 items-center w-full">
            <input
              type="text"
              v-model="minPrice"
              :disabled="isReadOnly"
              placeholder="e.g., Rp 50.000 or 'Free'"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'bg-[#F2F2F2]': isReadOnly }"
            />
            <Subtract class="min-w-2" />
            <input
              type="text"
              v-model="maxPrice"
              :disabled="isReadOnly"
              placeholder="e.g., Rp 100.000"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'bg-[#F2F2F2]': isReadOnly }"
            />
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <div class="space-x-2">
            <h3 class="text-base font-semibold">Contact</h3>
            <p class="text-sm font-medium text-neu-500">Opsional</p>
          </div>
          <label class="text-sm font-semibold">Phone Number</label>
          <input
            v-model="formData.contact_data.phone"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., +62 812 3456 7890"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.contact?.phone, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.contact?.phone" class="mt-1 text-xs text-red-500">
            {{ errors?.contact?.phone[0] }}
          </p>
          <label class="text-sm font-semibold mt-1">Mail</label>
          <input
            v-model="formData.contact_data.mail"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., info@spot.com"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.contact?.mail, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.contact?.mail" class="mt-1 text-xs text-red-500">
            {{ errors?.contact?.mail[0] }}
          </p>
        </div>

        <div class="flex flex-col gap-3">
          <div class="space-x-2">
            <h3 class="text-base font-semibold">Photos</h3>
            <p class="text-sm font-medium text-neu-500">
              {{
                isEditMode
                  ? 'Manage your destination images.'
                  : 'Upload at least 3 images for the destination.'
              }}
            </p>
          </div>

          <div class="w-full">
            <label
              for="imageUploadInput"
              class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed rounded-3xl cursor-pointer hover:bg-gray-200 transition"
              :class="{
                'border-blue-500 bg-blue-50': isDragging,
                'border-pr-500 bg-gray-100 hover:bg-gray-200': !isDragging,
                'border-red-500 bg-red-50': imageError,
              }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
            >
              <Photo
                class="mb-1 text-pr-500"
                :class="[isDragging ? 'text-blue-500' : '', imageError ? 'text-red-500' : '']"
              />

              <!-- Text -->
              <p
                class="font-medium text-sm mb-[2px] text-pr-500"
                :class="[isDragging ? 'text-blue-500' : '', imageError ? 'text-red-500' : '']"
              >
                Click to add photos
              </p>
              <p class="text-neu-900 text-sm">or drag & drop</p>

              <!-- Hidden input -->
              <!-- <input id="photo-upload" type="file" class="hidden" multiple /> -->
              <input
                type="file"
                id="imageUploadInput"
                @change="handleFileUpload"
                multiple
                accept="image/*"
                class="hidden"
                :disabled="isUploading"
              />
            </label>
            <p v-if="imageError" class="mt-2 text-xs text-red-500">
              {{ imageError }}
            </p>
          </div>
          <div v-if="galleryImages.length > 0" class="mt-2">
            <h4 class="text-base font-semibold mb-4">
              Current Gallery ({{ galleryImages.length }} images)
            </h4>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              <div
                v-for="image in galleryImages"
                :key="image.id"
                class="relative group aspect-square"
                :class="{
                  'ring-4 ring-offset-2 ring-pr-500 rounded-md': image.is_primary,
                  'ring-2 ring-red-500 ring-offset-2 rounded-md':
                    !image.isTemp && isMarkedForDeletion(image.id),
                }"
              >
                <img
                  :src="image.image_url"
                  :alt="image.alt_text || `image-${image.id}`"
                  class="w-full h-full object-cover rounded-md shadow-md"
                  :class="{
                    'opacity-40': !image.isTemp && isMarkedForDeletion(image.id),
                  }"
                />

                <div
                  v-if="image.is_primary"
                  class="absolute top-2 right-2 bg-pr-600 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg"
                >
                  Primary
                </div>

                <div
                  class="absolute inset-0 bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex flex-col items-center justify-center gap-2 p-2 rounded-md"
                >
                  <button
                    v-if="
                      isEditMode &&
                      !image.is_primary &&
                      !image.isTemp &&
                      !isMarkedForDeletion(image.id)
                    "
                    @click="handleSetPrimary(image)"
                    type="button"
                    class="opacity-0 group-hover:opacity-100 transition-opacity w-full text-center px-3 py-1 bg-blue-600 text-white text-xs rounded-full"
                  >
                    Set as Primary
                  </button>

                  <button
                    v-if="isEditMode && !image.isTemp"
                    @click="toggleDeletionMark(image)"
                    type="button"
                    class="opacity-0 group-hover:opacity-100 transition-opacity w-full text-center px-3 py-1 text-white text-xs rounded-full"
                    :class="isMarkedForDeletion(image.id) ? 'bg-yellow-500' : 'bg-red-600'"
                  >
                    {{ isMarkedForDeletion(image.id) ? 'Undo Delete' : 'Delete' }}
                  </button>

                  <button
                    v-if="image.isTemp"
                    @click="handleRemoveTempImage(image)"
                    type="button"
                    class="opacity-0 group-hover:opacity-100 transition-opacity w-full text-center px-3 py-1 bg-red-600 text-white text-xs rounded-full"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-sm text-gray-500 italic mt-2">No images have been uploaded yet.</p>
        </div>
      </div>

      <!-- Form Right -->
      <div
        class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl"
      >
        <!-- Map -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Map Location</label>
          <div class="w-full h-62 rounded-3xl overflow-hidden">
            <iframe
              class="w-full h-full"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>

        <!-- Street -->
        <div class="flex flex-col gap-3">
          <label for="street" class="text-base font-semibold">Street</label>
          <input
            id="street"
            v-model="formData.address_data.street"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Jalan Pantai Kuta"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{ 'border-red-500': errors?.address_data?.street, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.address_data?.street" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.street[0] }}
          </p>
        </div>

        <!-- Sub-district -->
        <div class="flex flex-col gap-3">
          <label for="sub_district" class="text-base font-semibold">Sub-district</label>
          <input
            id="sub_district"
            v-model="formData.address_data.sub_district"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Legian"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{
              'border-red-500': errors?.address_data?.sub_district,
              'bg-[#F2F2F2]': isReadOnly,
            }"
          />
          <p v-if="errors?.address_data?.sub_district" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.sub_district[0] }}
          </p>
        </div>
        <!-- District -->
        <div class="flex flex-col gap-3">
          <label for="district" class="text-base font-semibold">District</label>
          <input
            id="district"
            v-model="formData.address_data.district"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Kuta"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{
              'border-red-500': errors?.address_data?.district,
              'bg-[#F2F2F2]': isReadOnly,
            }"
          />
          <p v-if="errors?.address_data?.district" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.district[0] }}
          </p>
        </div>

        <!-- Regency -->
        <div class="flex flex-col gap-3">
          <label for="regency" class="text-base font-semibold">Regency</label>
          <input
            v-model="formData.address_data.regency"
            id="regency"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Badung"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{ 'border-red-500': errors?.address_data?.regency, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.address_data?.regency" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.regency[0] }}
          </p>
        </div>

        <!-- Latitude & Longitude -->
        <div class="flex flex-col gap-3">
          <div class="space-x-2">
            <h3 class="text-base font-semibold">Coordinate</h3>
            <p class="text-sm font-medium text-neu-500">Opsional</p>
          </div>
          <div class="flex flex-col sm:flex-row gap-6 sm:gap-4">
            <div class="flex flex-col gap-3 w-full">
              <label for="latitude" class="font-semibold text-sm mt-1">Latitude</label>
              <input
                v-model="formData.address_data.latitude"
                id="latitude"
                type="text"
                :disabled="isReadOnly"
                placeholder="e.g., -8.709201"
                class="px-3 py-3 text-sm border w-full placeholder:text-neu-500 border-neu-200 rounded-full"
                :class="{ 'bg-[#F2F2F2]': isReadOnly }"
              />
            </div>
            <div class="flex flex-col gap-3 w-full">
              <label for="longitude" class="font-semibold text-sm mt-1">Longitude</label>
              <input
                v-model="formData.address_data.longitude"
                id="longitude"
                type="text"
                :disabled="isReadOnly"
                placeholder="e.g., 115.168263"
                class="px-3 py-3 text-sm border w-full placeholder:text-neu-500 border-neu-200 rounded-full"
                :class="{ 'bg-[#F2F2F2]': isReadOnly }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-2.5 items-center">
      <button
        type="submit"
        :disabled="isLoading"
        :class="{ hidden: isReadOnly }"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
      >
        {{ isLoading ? 'Saving...' : isEditMode ? 'Save' : 'Create' }}
      </button>
      <RouterLink
        :to="{ name: 'AdminDestinations' }"
        type="button"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        {{ isReadOnly ? 'Back' : 'Cancel' }}
      </RouterLink>
    </div>
  </form>
</template>

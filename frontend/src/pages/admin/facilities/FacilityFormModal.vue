<script setup>
import { ref, computed, watchEffect } from 'vue'
import { useFacilityStore } from '@/stores/facilityStore'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'
import Upload from '@/components/icons/Upload.vue'

const props = defineProps({
  facilityData: {
    type: Object,
    default: null,
  },
})

const facilityStore = useFacilityStore()

const emit = defineEmits(['close', 'save'])

const form = ref({
  name: '',
})

const iconFile = ref(null) // Untuk objek File
const iconPreview = ref(null) // Untuk URL preview
const fileName = ref('') // Untuk nama file pratinjau
const fileSize = ref('') // Untuk ukuran file pratinjau
const isDragging = ref(false) // Untuk state drag-over

const formErrors = ref({})

const isEditMode = computed(() => !!(props.facilityData && props.facilityData.slug))

watchEffect(() => {
  if (props.facilityData && props.facilityData.slug) {
    form.value = {
      name: props.facilityData.name || '',
    }
    iconPreview.value = props.facilityData.icon_url || null
    iconFile.value = null
    fileName.value = props.facilityData.name
      ? `${props.facilityData.name.toLowerCase().replace(/\s+/g, '-')}.svg`
      : 'Current Icon'
    fileSize.value = ''
  } else {
    form.value = { name: '' }
    iconPreview.value = null
    iconFile.value = null
    fileName.value = ''
    fileSize.value = ''
  }

  formErrors.value = {}
  // facilityStore.clearError()
})

const handleFile = (file) => {
  if (!file) return

  formErrors.value.icon = undefined

  if (!file.name.toLowerCase().endsWith('.svg') || !file.type.includes('svg')) {
    formErrors.value.icon = ['Only .svg files are allowed.']
    return
  }

  // Validasi ukuran file
  if (file.size > 0.5 * 1024 * 1024) {
    // 500KB
    formErrors.value.icon = ['Icon image size cannot exceed 500KB.']
    return
  }

  iconFile.value = file // Simpan objek File untuk di-upload
  fileName.value = file.name
  fileSize.value = (file.size / 1024).toFixed(2) + ' KB'
  iconPreview.value = URL.createObjectURL(file) // Buat URL lokal untuk pratinjau
}
//  AKHIR PENAMBAHAN

//  PERUBAHAN: Disederhanakan untuk memanggil handleFile
const handleIconUpload = (event) => {
  const file = event.target.files?.[0]
  handleFile(file)
}
//  AKHIR PERUBAHAN

//  PENAMBAHAN: Handler untuk drag-and-drop
const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files?.[0]
  handleFile(file)
}

const removeIcon = () => {
  iconPreview.value = null
  iconFile.value = null
  fileName.value = ''
  fileSize.value = ''
  // Reset input file agar bisa memilih file yang sama lagi
  const input = document.getElementById('facility-icon-input')
  if (input) {
    input.value = ''
  }
}
//  AKHIR PENAMBAHAN

const submitForm = async () => {
  formErrors.value = {}

  if (!form.value.name.trim()) {
    formErrors.value.name = ['Facility name is required.']
    return
  }
  if (!isEditMode.value && !iconFile.value) {
    formErrors.value.icon = ['SVG Icon file is required.']
    return
  }
  // Validasi file sudah ditangani oleh handleFile, jadi bisa dihapus dari sini

  const formDataPayload = new FormData()
  formDataPayload.append('name', form.value.name)

  if (iconFile.value) {
    formDataPayload.append('icon', iconFile.value, iconFile.value.name)
  }

  const dataToEmit = { payload: formDataPayload }

  if (isEditMode.value) {
    dataToEmit.identifier = props.facilityData.slug
  }

  emit('save', dataToEmit)
}

const handleClose = () => {
  emit('close')
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999999"
  >
    <div class="bg-white px-4 pt-4 pb-8 flex-col flex rounded-3xl w-full max-w-150 animate-fadeIn">
      <div class="flex justify-end w-full">
        <Exit
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(true)"
        />
      </div>
      <form @submit.prevent="submitForm" class="w-full flex flex-col mt-4 space-y-6 px-4">
        <div class="flex flex-col gap-1">
          <h1 class="text-3xl font-se font-semibold">
            {{ isEditMode ? 'Edit Facility' : 'Create Facility' }}
          </h1>
          <div class="flex gap-2 items-center text-sm font-medium">
            <span>Katalog</span>
            <ArrowRight class="size-4 text-neu-500" />
            <RouterLink :to="{ name: 'AdminFacilities' }" class="hover:underline"
              >Facilities</RouterLink
            >
            <ArrowRight class="size-4 text-neu-500" />
            <span class="text-neu-500">{{ isEditMode ? 'Edit' : 'Create' }}</span>
          </div>
        </div>
        <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col flex-1 gap-4">
          <div class="flex flex-col gap-3">
            <label for="facility-name" class="text-base font-semibold">Facility Name</label>
            <input
              type="text"
              id="facility-name"
              v-model="form.name"
              placeholder="Name"
              required
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'border-red-500': formErrors.name }"
            />
            <p v-if="formErrors.name" class="mt-1 text-xs text-red-500">
              {{ formErrors.name.join(', ') }}
            </p>
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-base font-semibold">SVG Icon File</label>

            <div v-if="!iconPreview">
              <label
                for="facility-icon-input"
                class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed rounded-3xl cursor-pointer"
                :class="{
                  'border-blue-500 bg-blue-50': isDragging,
                  'border-pr-500 bg-gray-100 hover:bg-gray-200': !isDragging,
                  'border-red-500 bg-red-50': formErrors.icon,
                }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
              >
                <div class="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload class="size-7 md:size-9 mb-4 text-neu-500" />
                  <p class="mb-2 text-sm text-neu-500">
                    <span class="font-semibold">Click to upload</span> or drag and drop
                  </p>
                  <p class="text-xs text-neu-500">SVG only (MAX. 500KB)</p>
                </div>
              </label>
            </div>

            <div
              v-else
              class="flex items-center justify-between w-full ps-5 pe-3 py-3 text-sm border border-neu-200 rounded-full"
            >
              <div class="flex items-center gap-3 overflow-hidden">
                <img
                  :src="iconPreview"
                  alt="Icon preview"
                  class="h-10 w-10 object-contain flex-shrink-0"
                />
                <div class="overflow-hidden">
                  <p class="font-medium text-neu-900 truncate">{{ fileName }}</p>
                  <p class="text-xs mt-0.5 text-neu-500">{{ fileSize }}</p>
                </div>
              </div>
              <button
                @click="removeIcon"
                type="button"
                class="text-gray-500 hover:text-red-600 p-1"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  ></path>
                </svg>
              </button>
            </div>

            <input
              type="file"
              id="facility-icon-input"
              @change="handleIconUpload"
              :required="!isEditMode && !iconFile"
              accept=".svg"
              class="hidden"
            />

            <p v-if="formErrors.icon" class="mt-1 text-xs text-red-500">
              {{ Array.isArray(formErrors.icon) ? formErrors.icon.join(', ') : formErrors.icon }}
            </p>
          </div>
        </div>

        <p
          v-if="
            formErrors.general ||
            (facilityStore?.facilityError &&
              !Object.keys(formErrors).filter((k) => k !== 'general').length)
          "
          class="text-sm text-red-500"
        >
          {{
            (formErrors.general && formErrors.general[0]) ||
            facilityStore?.facilityError.name[0] ||
            'An error occurred.'
          }}
        </p>
        <div class="flex gap-2.5 items-center">
          <button
            type="submit"
            :disabled="facilityStore.isLoadingFacilities"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            {{ facilityStore.isLoadingFacilities ? 'Saving...' : 'Save' }}
          </button>
          <button
            type="button"
            @click="handleClose"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style>

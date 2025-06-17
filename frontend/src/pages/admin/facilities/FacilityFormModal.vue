<script setup>
import { ref, computed, watchEffect } from 'vue'
import { useFacilityStore } from '@/stores/facilityStore'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'

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

const formErrors = ref({})

const isEditMode = computed(() => !!(props.facilityData && props.facilityData.slug))

watchEffect(() => {
  if (props.facilityData && props.facilityData.slug) {
    form.value = {
      name: props.facilityData.name || '',
    }
    iconPreview.value = props.facilityData.icon_url || null
    iconFile.value = null //
  } else {
    form.value = { name: '' }
    iconPreview.value = null
    iconFile.value = null
  }

  formErrors.value = {}
  // facilityStore.clearError()
})

const handleIconUpload = (event) => {
  const file = event.target.files[0]
  formErrors.value.icon = undefined // Hapus error field ikon sebelumnya

  if (file) {
    if (!file.name.toLowerCase().endsWith('.svg')) {
      formErrors.value.icon = ['Only .svg files are allowed.']
      iconFile.value = null
      event.target.value = null // Reset input file
      return
    }
    if (file.size > 0.5 * 1024 * 1024) {
      // 500KB
      formErrors.value.icon = ['Icon image size cannot exceed 500KB.']
      iconFile.value = null
      event.target.value = null
      return
    }
    iconFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      iconPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
    // removeCurrentImage.value = false; // Jika ada file baru, jangan hapus gambar
  } else {
    // Jika pengguna membatalkan pemilihan file
    iconFile.value = null
    // Kembalikan preview ke gambar yang ada (jika edit) atau null (jika create)
    if (isEditMode.value) {
      iconPreview.value = props.facilityData?.icon_url || null
    } else {
      iconPreview.value = null
    }
  }
}

const submitForm = async () => {
  formErrors.value = {}
  // facilityStore.clearError()
  try {
    // Validasi frontend dasar
    if (!form.value.name.trim()) {
      formErrors.value.name = ['Facility name is required.']
      return
    }
    if (!isEditMode.value && !iconFile.value) {
      // Ikon wajib saat create
      formErrors.value.icon = ['SVG Icon file is required.']
      return
    }
    // Validasi tambahan untuk file ikon jika ada file baru dipilih (sudah di handleIconUpload)
    if (iconFile.value) {
      if (!iconFile.value.name.toLowerCase().endsWith('.svg')) {
        formErrors.value.icon = ['Only .svg files are allowed.']
        return
      }
      if (iconFile.value.size > 0.5 * 1024 * 1024) {
        // 500KB
        formErrors.value.icon = ['Icon image size cannot exceed 500KB.']
        return
      }
    }

    // Selalu gunakan FormData karena ada potensi upload file ikon
    const formDataPayload = new FormData()
    formDataPayload.append('name', form.value.name)

    // ICON IMAGE:
    // Hanya append 'icon' jika ada file BARU yang dipilih.
    // Jika mode edit dan tidak ada file baru dipilih, backend akan mempertahankan gambar lama.
    // Jika mode create, file baru wajib (sudah divalidasi di atas).
    if (iconFile.value) {
      formDataPayload.append('icon', iconFile.value, iconFile.value.name)
    }
    const dataToEmit = {
      payload: formDataPayload, // Ini adalah FormData
    }

    if (isEditMode.value) {
      // Saat edit, kita emit SLUG dari props.facilityData (slug LAMA sebelum potensi perubahan nama)
      // karena ini yang akan digunakan untuk membangun URL API update.
      dataToEmit.identifier = props.facilityData.slug
    }

    console.log(formDataPayload)

    // Emit event 'save' dengan objek yang berisi 'payload' dan 'identifier' (jika edit)
    emit('save', dataToEmit) // Emit event save dengan data form
  } catch (error) {
    if (error && typeof error === 'object' && !Array.isArray(error) && !(error instanceof Error)) {
      formErrors.value = error
    } else {
      // Untuk error umum lainnya, mungkin set pesan error umum.
      // Namun, ini lebih baik ditangani oleh parent dengan toast.
      console.error('Error during form submission process in modal:', error)
      formErrors.value = { general: [error?.message || 'Submission failed.'] }
    }
  }
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
          <div class="flex flex-col gap-3">
            <label for="facility-icon" class="text-base font-semibold">SVG Icon File</label>
            <input
              type="file"
              id="facility-icon"
              @change="handleIconUpload"
              :required="!isEditMode"
              accpet=".svg"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'border-red-500': formErrors.icon }"
            />
            <div v-if="iconPreview" class="mt-2">
              <img :src="iconPreview" alt="Icon preview" class="h-16 w-16 object-contain" />
            </div>
            <p v-if="formErrors.icon" class="mt-1 text-xs text-red-500">
              {{ formErrors.icon.join(', ') }}
            </p>
          </div>
        </div>
        <!-- Tampilkan error umum dari store -->
        <p
          v-if="
            formErrors.general ||
            (facilityStore &&
              facilityStore.facilityError &&
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

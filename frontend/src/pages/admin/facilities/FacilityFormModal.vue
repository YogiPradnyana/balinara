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
  id: null,
  name: '',
  icon_url: '',
  slug: '',
})

const formErrors = ref({})

const isEditMode = computed(() => !!form.value.id)

watchEffect(() => {
  if (props.facilityData) {
    form.value = { ...props.facilityData }
  } else {
    form.value = { id: null, name: '', icon_url: '', slug: '' }
  }
  formErrors.value = {}
  facilityStore.clearError()
})

const submitForm = async () => {
  formErrors.value = {}
  facilityStore.clearError()
  try {
    const payload = {
      name: form.value.name,
    }
    if (form.value.icon_url) {
      payload.icon_url = form.value.icon_url
    }

    if (form.value.slug) {
      // Hanya kirim slug jika diisi, biarkan backend generate jika tidak
      payload.slug = form.value.slug
    }

    if (isEditMode.value) {
      payload.id = form.value.id
    }

    await emit('save', payload) // Emit event save dengan data form
  } catch (error) {
    if (error && typeof error === 'object' && !Array.isArray(error) && !(error instanceof Error)) {
      formErrors.value = error
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
            <label for="facility-icon" class="text-base font-semibold">SVG</label>
            <textarea
              id="facility-icon"
              rows="7"
              required
              placeholder="SVG Tag"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
              v-model="form.icon_url"
              :class="{ 'border-red-500': formErrors.icon_url }"
            ></textarea>
            <p v-if="formErrors.icon_url" class="mt-1 text-xs text-red-500">
              {{ formErrors.icon_url.join(', ') }}
            </p>
          </div>
        </div>
        <!-- Tampilkan error umum dari store -->
        <p
          v-if="facilityStore.facilityError && !Object.keys(formErrors).length"
          class="text-sm text-red-500"
        >
          {{ facilityStore.facilityError.name[0] }}
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

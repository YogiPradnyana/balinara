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
  </div>
</template>

<script setup lang="ts">
import ArrowRight from '@/components/icons/ArrowRight.vue'
import { useRouter, RouterLink } from 'vue-router'
import { ref } from 'vue'
import { useDestinationStore } from '@/stores/destinationStore'
import DestinationForm from '@/components/admin/destinations/DestinationForm.vue'
import { showNotification } from '@/services/notificationService'

const destinationStore = useDestinationStore()
const router = useRouter()
const formErrors = ref(null)

async function handleCreateDestination(formData) {
  formErrors.value = null
  try {
    await destinationStore.createDestination(formData)
    showNotification('success', 'Destination added successfully')
    router.push({ name: 'AdminDestinations' })
  } catch (error) {
    formErrors.value = error
    showNotification('error', 'Failed to create destination. Please check the form for errors.')
    console.error('Full error response:', error)
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Create Destination</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminDestinations' }" class="hover:underline"
          >Destinations</RouterLink
        >
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Create</span>
      </div>
    </div>
    <DestinationForm
      @submit="handleCreateDestination"
      :is-loading="destinationStore.isLoadingDetail"
      :errors="formErrors"
    />
  </div>
</template>

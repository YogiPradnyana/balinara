<script setup lang="ts">
import ArrowRight from '@/components/icons/ArrowRight.vue'
import { RouterLink } from 'vue-router'
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDestinationStore } from '@/stores/destinationStore'
import DestinationForm from '@/components/admin/destinations/DestinationForm.vue'
import Edit from '@/components/icons/Edit.vue'

const store = useDestinationStore()
const route = useRoute()

// Ambil data lama saat halaman dimuat
onMounted(() => {
  const slug = route.params.slug
  store.fetchDestinationBySlug(slug)
})

const isLoading = computed(() => store.isLoadingDetail)
const destinationToRead = computed(() => store.currentDestination)
</script>

<template>
  <div v-if="isLoading" class="p-8 text-center text-gray-500">Loading Destination...</div>
  <div v-else-if="destinationToRead" class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Detail Destination</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Katalog</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminDestinations' }" class="hover:underline"
          >Destinations</RouterLink
        >
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Detail</span>
      </div>
    </div>
    <RouterLink
      :to="{ name: 'AdminDestinationEdit', params: { slug: destinationToRead.slug } }"
      class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
    >
      <Edit class="size-5" />
      Edit Destination
    </RouterLink>
    <DestinationForm
      v-if="destinationToRead"
      :initial-data="destinationToRead"
      :is-read-only="true"
      :is-edit-mode="true"
    />
  </div>
</template>

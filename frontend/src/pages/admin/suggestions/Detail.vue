<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useSuggestionStore } from '@/stores/suggestionStore'
import { showNotification } from '@/services/notificationService'

// Impor ikon
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowRight from '@/components/icons/ArrowRight.vue'

// Impor komponen peta dan CSS Leaflet
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import { icon } from 'leaflet';

// Fix untuk ikon marker default Leaflet
const defaultIcon = icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const route = useRoute()
const router = useRouter()
const suggestionStore = useSuggestionStore()

const isSaving = ref(false)
const selectedStatus = ref('')

const suggestion = computed(() => suggestionStore.suggestionDetail)

const mapCoordinates = computed(() => {
  if (suggestion.value && suggestion.value.latitude && suggestion.value.longitude) {
    return [suggestion.value.latitude, suggestion.value.longitude];
  }
  return [-8.409518, 115.188919];
});
const mapZoom = computed(() => {
    return (suggestion.value && suggestion.value.latitude) ? 14 : 8;
})

watch(suggestion, (newSuggestion) => {
  if (newSuggestion) {
    selectedStatus.value = newSuggestion.status
  }
})

onMounted(() => {
  const suggestionId = route.params.id
  if (suggestionId && suggestionId !== 'undefined') {
    suggestionStore.fetchSuggestionDetail(suggestionId)
  } else {
    router.push({ name: 'AdminSuggestions' })
  }
})

const handleUpdateStatus = async () => {
    if (!suggestion.value || !suggestion.value.id) {
        alert("Data detail belum dimuat dengan benar. Silakan refresh halaman.");
        return;
    }
    isSaving.value = true
    try {
        await suggestionStore.updateSuggestionStatus(suggestion.value.id, selectedStatus.value)
        showNotification('success', 'Status suggestion berhasil diperbarui.')
    } catch (error) {
        showNotification('error', 'Gagal memperbarui status.')
    } finally {
        isSaving.value = false
    }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Detail Suggested Spot</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminSuggestions' }" class="hover:underline">Suggestions</RouterLink>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Detail</span>
      </div>
    </div>

    <div v-if="suggestionStore.isLoading && !suggestion">Memuat data detail...</div>
    <div v-else-if="suggestionStore.error" class="text-red-500">Gagal memuat data. {{ suggestionStore.error }}</div>
    
    <div v-else-if="suggestion">
        <form @submit.prevent="handleUpdateStatus" class="flex flex-col lg:flex-row gap-6 lg:gap-8">
            <!-- Kolom Kiri -->
            <div class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl">
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Name</label>
                    <input type="text" :value="suggestion.name" disabled class="px-3 py-3 text-sm border bg-gray-100 rounded-full"/>
                </div>
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Traveler Name</label>
                    <input type="text" :value="suggestion.suggester_username" disabled class="px-3 py-3 text-sm border bg-gray-100 rounded-full"/>
                </div>
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Status</label>
                    <div class="relative w-full">
                        <select v-model="selectedStatus" class="w-full px-3 py-3 text-sm border rounded-full appearance-none focus:ring-2 focus:ring-pr-500">
                            <option value="pending">Pending</option>
                            <option value="approved">Approved</option>
                            <option value="rejected">Rejected</option>
                        </select>
                        <ArrowDown class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none"/>
                    </div>
                </div>
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Category</label>
                    <input type="text" :value="suggestion.category_name" disabled class="px-3 py-3 text-sm border bg-gray-100 rounded-full"/>
                </div>
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Descriptions</label>
                    <textarea :value="suggestion.descriptions" rows="7" disabled class="px-3 py-3 text-sm border bg-gray-100 rounded-3xl"></textarea>
                </div>
                
                <!-- ================================================================= -->
                <!-- PERBAIKAN UTAMA ADA DI SINI -->
                <!-- Menggunakan 'suggestion.facilities_details' sebagai sumber data -->
                <!-- ================================================================= -->
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Facilities</label>
                    <ul v-if="suggestion.facilities_details && suggestion.facilities_details.length > 0" class="flex flex-wrap text-sm sm:text-base gap-3 sm:gap-4">
                        <li
                            v-for="facility in suggestion.facilities_details"
                            :key="facility.id"
                            class="bg-gray-100 text-gray-800 font-medium items-center px-4 py-2 rounded-full flex"
                        >
                            {{ facility.name }}
                        </li>
                    </ul>
                    <p v-else class="text-sm text-gray-500">No facilities listed.</p>
                </div>
                <!-- ================================================================= -->

                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Photos</label>
                    <div class="flex flex-wrap gap-4">
                        <a v-for="photo in suggestion.photos" :key="photo.id" :href="photo.image" target="_blank">
                            <img :src="photo.image" :alt="suggestion.name" class="object-cover w-40 h-24 rounded-lg border hover:opacity-80 transition"/>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Kolom Kanan (Address, Map, dll) -->
            <div class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl">
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Map Location</label>
                    <div class="w-full h-62 rounded-3xl overflow-hidden border">
                        <l-map
                            v-if="suggestion"
                            :zoom="mapZoom"
                            :center="mapCoordinates"
                            :use-global-leaflet="false"
                            style="height: 100%; width: 100%"
                        >
                            <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" attribution="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"></l-tile-layer>
                            <l-marker v-if="suggestion.latitude && suggestion.longitude" :lat-lng="mapCoordinates" :icon="defaultIcon"></l-marker>
                        </l-map>
                    </div>
                </div>
                <div class="flex flex-col gap-3">
                    <label class="text-base font-semibold">Address</label>
                    <input type="text" :value="`${suggestion.street || ''}, ${suggestion.sub_district || ''}, ${suggestion.regency || ''}`.replace(/^,|,$/g, '').trim()" disabled class="px-3 py-3 text-sm border bg-gray-100 rounded-full"/>
                </div>
                <div class="flex gap-4">
                    <div class="flex flex-col gap-3 w-1/2">
                        <label class="font-semibold text-sm">Latitude</label>
                        <input type="text" :value="suggestion.latitude" disabled class="px-3 py-3 text-sm w-full border bg-gray-100 rounded-full"/>
                    </div>
                    <div class="flex flex-col gap-3 w-1/2">
                        <label class="font-semibold text-sm">Longitude</label>
                        <input type="text" :value="suggestion.longitude" disabled class="px-3 py-3 text-sm w-full border bg-gray-100 rounded-full"/>
                    </div>
                </div>
            </div>
        </form>

        <div class="mt-8 flex gap-4 items-center">
            <button
                @click="handleUpdateStatus"
                :disabled="isSaving"
                type="button"
                class="px-6 py-3 text-white bg-pr-500 hover:bg-pr-600 rounded-full font-medium disabled:bg-gray-400"
            >
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
            <RouterLink :to="{ name: 'AdminSuggestions' }" type="button" class="px-6 py-3 text-neu-900 bg-gray-100 hover:bg-gray-200 rounded-full font-medium">
                Back
            </RouterLink>
        </div>
    </div>
  </div>
</template>

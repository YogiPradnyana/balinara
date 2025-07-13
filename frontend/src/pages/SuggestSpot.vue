<script setup>
import { ref, onMounted } from 'vue';
// Impor store dan service
import { useCategoryStore } from '@/stores/categoryStore';
import { useFacilityStore } from '@/stores/facilityStore';
import { useSuggestionStore } from '@/stores/suggestionStore';
import suggestionService from '@/services/suggestionService';

// Impor lain-lain
import { showNotification } from '@/services/notificationService';
import { useRouter } from 'vue-router';
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import { icon } from 'leaflet';

// Impor ikon
import Photo from '@/components/icons/Photo.vue';
import Subtract from '@/components/icons/Subtract.vue';

// --- Konfigurasi dan State ---
const router = useRouter();
const categoryStore = useCategoryStore();
const facilityStore = useFacilityStore();
const suggestionStore = useSuggestionStore();

const isLoading = ref(false);
const isUploading = ref(false);

const initialFormData = {
  name: '', category: null, descriptions: '', entrance_ticket_min: '',
  entrance_ticket_max: '', phone_number: '', email: '', street: '',
  sub_district: '', regency: '', latitude: '', longitude: '',
  selectedFacilities: [], temp_photo_ids: []
};
const formData = ref({ ...initialFormData });

const uploadedImages = ref([]); 
const minPhotosRequired = 3;

// State Peta
const zoom = ref(10);
const mapCenter = ref([-8.65, 115.216667]);
const markerLatLng = ref(null);
const defaultIcon = icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41], iconAnchor: [12, 41],
});

// --- Lifecycle & Methods ---
onMounted(() => {
  categoryStore.fetchCategories();
  facilityStore.fetchFacilities();
});

function handleMapClick(mapEvent) {
  const { lat, lng } = mapEvent.latlng;
  formData.value.latitude = lat.toFixed(6);
  formData.value.longitude = lng.toFixed(6);
  markerLatLng.value = [lat, lng];
}

async function handleFileChange(event) {
  const files = Array.from(event.target.files);
  isUploading.value = true;
  try {
    for (const file of files) {
      if (file.type.startsWith('image/')) {
        const response = await suggestionService.uploadTemporaryImage(file);
        formData.value.temp_photo_ids.push(response.data.id);
        uploadedImages.value.push({ id: response.data.id, url: response.data.image });
      }
    }
  } catch (error) {
    showNotification('error', 'Image upload failed.');
  } finally {
    isUploading.value = false;
  }
}

function removePhoto(index, photoId) {
  uploadedImages.value.splice(index, 1);
  formData.value.temp_photo_ids = formData.value.temp_photo_ids.filter(id => id !== photoId);
}

function resetForm() {
  formData.value = { ...initialFormData };
  uploadedImages.value = [];
  markerLatLng.value = null;
}

async function suggestSpot() {
  isLoading.value = true;
  const payload = { ...formData.value };
  payload.facilities = payload.selectedFacilities;
  delete payload.selectedFacilities;

  try {
    await suggestionStore.createSuggestion(payload);
    showNotification('success', 'Thank you! Your suggestion has been received.');
    resetForm();
    
    // =================================================================
    // PASTIKAN NAMA RUTE DI SINI SAMA DENGAN DI router/index.js
    // =================================================================
    router.push({ name: 'UserSuggestion' });

  } catch (error) {
    showNotification('error', 'Failed to submit suggestion. Please check the form.');
    console.error('Submit suggestion error:', error);
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <form class="flex flex-col lg:flex-row gap-6 lg:gap-16 mt-10 md:mt-16" @submit.prevent="suggestSpot">
      <!-- Kolom Kiri -->
      <div class="w-full md:w-3/4 lg:min-w-80 xl:min-w-120 flex flex-col gap-6">
        <h1 class="text-4xl sm:text-[42px] font-semibold leading-12 sm:leading-[62px] font-se">
          <span class="text-pr-500">Suggest a Spot</span> & Inspire Travelers!
        </h1>

        <!-- Spot Name -->
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Spot Name</label>
          <input v-model="formData.name" type="text" id="name" placeholder="e.g., Hidden Gem Beach Club" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" required />
        </div>

        <!-- Category (Radio Buttons) -->
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Category</label>
          <div v-if="categoryStore.isLoading">Loading categories...</div>
          <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <label v-for="cat in categoryStore.allCategories" :key="cat.id" 
                   class="flex items-center gap-2 p-3 border rounded-lg cursor-pointer transition-colors"
                   :class="formData.category === cat.id ? 'bg-pr-50 border-pr-500 ring-2 ring-pr-200' : 'border-neu-200 hover:bg-gray-50'">
              <input 
                type="radio" 
                name="category"
                :value="cat.id"
                v-model="formData.category"
                class="h-4 w-4 text-pr-600 focus:ring-pr-500 border-gray-300"
              />
              <span class="text-sm font-medium text-neu-800">{{ cat.name }}</span>
            </label>
          </div>
        </div>

        <!-- Description -->
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold">Description</label>
          <textarea v-model="formData.descriptions" id="descriptions" rows="7" placeholder="Tell us what makes this place special..." class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl" required></textarea>
        </div>

        <!-- Entrance Ticket -->
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Entrance Ticket Price Range</label>
          <div class="flex gap-2.5 items-center w-full">
            <input v-model="formData.entrance_ticket_min" type="number" placeholder="e.g., 75000" class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full" />
            <Subtract class="min-w-2" />
            <input v-model="formData.entrance_ticket_max" type="number" placeholder="e.g., 120000" class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full" />
          </div>
        </div>

        <!-- Contact -->
        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Contact</h3>
          <label class="font-semibold">Phone Number</label>
          <input v-model="formData.phone_number" type="text" placeholder="e.g., +62 812 3456 7890" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
          <label class="font-semibold mt-1">Email</label>
          <input v-model="formData.email" type="email" placeholder="e.g., info@spot.com" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
      </div>

      <!-- Kolom Kanan -->
      <div class="w-full md:w-3/4 lg:w-full flex flex-col gap-6">
        
        <!-- Map Location -->
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Select Location on Map</label>
          <p class="text-sm text-neu-700">Click on the map to automatically set the Latitude & Longitude.</p>
          <div class="w-full h-80 xl:h-[400px] rounded-3xl overflow-hidden border">
            <l-map v-model:zoom="zoom" :center="mapCenter" @click="handleMapClick" style="height: 100%; width: 100%">
              <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" attribution="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"></l-tile-layer>
              <l-marker v-if="markerLatLng" :lat-lng="markerLatLng" :icon="defaultIcon"></l-marker>
            </l-map>
          </div>
        </div>

        <!-- Address -->
        <div class="flex flex-col gap-3">
          <label for="street" class="text-base md:text-lg font-semibold">Street</label>
          <input v-model="formData.street" type="text" id="street" placeholder="e.g., Jl. Pantai Kuta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
        <div class="flex flex-col gap-3">
          <label for="sub-district" class="text-base md:text-lg font-semibold">Sub-district</label>
          <input v-model="formData.sub_district" type="text" id="sub-district" placeholder="e.g., Kuta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
        <div class="flex flex-col gap-3">
          <label for="regency" class="text-base md:text-lg font-semibold">Regency</label>
          <input v-model="formData.regency" type="text" id="regency" placeholder="e.g., Badung" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>

        <!-- Coordinates -->
        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Coordinates</h3>
          <div class="flex gap-6">
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Latitude</label>
              <input v-model="formData.latitude" type="text" placeholder="Auto-filled from map" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
            </div>
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Longitude</label>
              <input v-model="formData.longitude" type="text" placeholder="Auto-filled from map" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
            </div>
          </div>
        </div>

        <!-- Facilities (Checkboxes) -->
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Facilities</label>
          <div v-if="facilityStore.isLoading">Loading facilities...</div>
          <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-3">
             <label v-for="fac in facilityStore.allFacilities" :key="fac.id" 
                   class="flex items-center gap-2 p-3 border rounded-lg cursor-pointer transition-colors"
                   :class="formData.selectedFacilities.includes(fac.id) ? 'bg-pr-50 border-pr-500 ring-2 ring-pr-200' : 'border-neu-200 hover:bg-gray-50'">
              <input 
                type="checkbox"
                :value="fac.id"
                v-model="formData.selectedFacilities"
                class="h-4 w-4 rounded text-pr-600 focus:ring-pr-500 border-gray-300"
              />
              <span class="text-sm font-medium text-neu-800">{{ fac.name }}</span>
            </label>
          </div>
        </div>

        <!-- Photos -->
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Photos</label>
          <p class="text-sm text-neu-700">Upload at least {{ minPhotosRequired }} images for the destination.</p>
          <div class="w-full">
            <label for="photo-upload" class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition">
              <span v-if="isUploading">Uploading...</span>
              <div v-else>
                <Photo class="mx-auto mb-1" />
                <p class="text-pr-500 font-medium text-sm mb-[2px]">Click to add photos</p>
                <p class="text-neu-900 text-sm">or drag & drop</p>
              </div>
              <input id="photo-upload" type="file" class="hidden" multiple @change="handleFileChange" accept="image/*" :disabled="isUploading" />
            </label>
          </div>
          <div v-if="uploadedImages.length > 0" class="mt-6">
            <h3 class="text-base md:text-lg font-semibold">Current Gallery ({{ uploadedImages.length }} images)</h3>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4">
              <div v-for="(image, index) in uploadedImages" :key="image.id" class="relative group">
                <img :src="image.url" alt="Uploaded photo" class="w-full h-28 object-cover rounded-lg shadow-md" />
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-300 flex items-center justify-center">
                  <button type="button" class="px-3 py-1 bg-red-600 text-white text-xs font-bold rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" @click="removePhoto(index, image.id)">Remove</button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="mt-2 text-sm text-gray-500">
            You need to upload at least {{ minPhotosRequired }} images.
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading || isUploading || formData.temp_photo_ids.length < minPhotosRequired"
          class="bg-pr-500 text-neu-50 px-6 text-base sm:text-lg py-4 font-medium rounded-full hover:bg-pr-600 disabled:bg-neu-300 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Submitting...' : 'Suggest This Spot' }}
        </button>
      </div>
    </form>
  </div>
</template>

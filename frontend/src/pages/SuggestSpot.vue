<script setup>
import { ref, onMounted } from 'vue';

// Impor store yang akan kita gunakan
import { useCategoryStore } from '@/stores/categoryStore';
import { useFacilityStore } from '@/stores/facilityStore';
import { useSuggestionStore } from '@/stores/suggestionStore';

// Impor notifikasi dan semua ikon yang dibutuhkan
import { showNotification } from '@/services/notificationService';
import ArrowDown from '@/components/icons/ArrowDown.vue';
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue';
import Exit from '@/components/icons/Exit.vue';
import Photo from '@/components/icons/Photo.vue';
import Subtract from '@/components/icons/Subtract.vue';

// Impor komponen peta dan CSS Leaflet
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import { icon } from 'leaflet';

// State untuk peta
const zoom = ref(10);
const mapCenter = ref([-8.65, 115.216667]); // Titik tengah peta di Denpasar
const markerLatLng = ref(null); // Posisi marker (penanda)

// Fungsi yang dijalankan saat peta diklik
function handleMapClick(mapEvent) {
  const lat = mapEvent.latlng.lat;
  const lng = mapEvent.latlng.lng;
  formData.value.latitude = lat.toFixed(6);
  formData.value.longitude = lng.toFixed(6);
  markerLatLng.value = [lat, lng];
}

// Fix untuk ikon marker default Leaflet
const defaultIcon = icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// Inisialisasi store
const categoryStore = useCategoryStore();
const facilityStore = useFacilityStore();
const suggestionStore = useSuggestionStore();

// State lokal untuk halaman ini
const isLoading = ref(false);
const initialFormData = {
  name: '', category: null, descriptions: '', entrance_ticket_min: '',
  entrance_ticket_max: '', phone_number: '', email: '', street: '',
  sub_district: '', regency: '', latitude: '', longitude: '',
  selectedFacilities: [], photos: []
};
const formData = ref({ ...initialFormData });
const uploadedImageUrls = ref([]);
const minPhotosRequired = 3;

// Saat halaman pertama kali dimuat, panggil store untuk mengambil data
onMounted(() => {
  categoryStore.fetchCategories();
  facilityStore.fetchFacilities();
});

// Fungsi bantuan untuk interaksi form
function handleFileChange(event) {
  const files = Array.from(event.target.files);
  formData.value.photos.push(...files);
  for (const file of files) {
    const reader = new FileReader();
    reader.onload = (e) => uploadedImageUrls.value.push(e.target.result);
    reader.readAsDataURL(file);
  }
}
function removePhoto(index) {
  formData.value.photos.splice(index, 1);
  uploadedImageUrls.value.splice(index, 1);
}
function addFacility(event) {
  const facilityId = event.target.value;
  if (facilityId && !formData.value.selectedFacilities.includes(facilityId)) {
    formData.value.selectedFacilities.push(facilityId);
  }
  event.target.value = '';
}
function removeFacility(facilityId) {
  formData.value.selectedFacilities = formData.value.selectedFacilities.filter(id => id !== facilityId);
}
function getFacilityName(facilityId) {
  const facility = facilityStore.facilities.find(f => f.id == facilityId);
  return facility ? facility.name : '';
}

// Fungsi untuk mereset semua isian form ke keadaan awal
function resetForm() {
  formData.value = { ...initialFormData };
  uploadedImageUrls.value = [];
  markerLatLng.value = null;
}

// Fungsi utama yang dijalankan saat tombol "Submit" diklik
async function suggestSpot() {
  isLoading.value = true;
  const submissionData = new FormData();
  Object.keys(formData.value).forEach(key => {
    const value = formData.value[key];
    if (key === 'photos') value.forEach(file => submissionData.append('uploaded_photos', file));
    else if (key === 'selectedFacilities') value.forEach(id => submissionData.append('facilities', id));
    else if (value !== null && value !== '') submissionData.append(key, value);
  });
  try {
    await suggestionStore.createSuggestion(submissionData);
    // Notifikasi akan terlihat
    showNotification('success', 'Terima kasih! Saran Anda telah kami terima.');
    // Panggil fungsi reset sebagai ganti reload
    resetForm();
  } catch (error) {
    showNotification('error', 'Gagal mengirim saran. Silakan periksa kembali isian Anda.');
    console.error('Error:', error.response?.data || error.message);
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <form class="flex flex-col lg:flex-row gap-6 lg:gap-16 mt-10 md:mt-16" @submit.prevent="suggestSpot">
      <div class="w-full md:w-3/4 lg:min-w-80 xl:min-w-120 flex flex-col gap-6">
        <h1 class="text-4xl sm:text-[42px] font-semibold leading-12 sm:leading-[62px] font-se">
          <span class="text-pr-500">Sarankan</span> Tempat & Inspirasi Wisatawan!
        </h1>

        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Nama Tempat</label>
          <input v-model="formData.name" type="text" id="name" placeholder="cth: Hidden Gem Beach Club" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" required />
        </div>

        <div class="flex flex-col gap-3">
          <label for="category" class="text-base md:text-lg font-semibold">Kategori</label>
          <div class="relative w-full">
            <select v-model="formData.category" id="category" class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none" required>
              <option :value="null" disabled>Pilih kategori...</option>
              <option v-for="cat in categoryStore.allCategories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
            <ArrowDown class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400" />
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold">Deskripsi</label>
          <textarea v-model="formData.descriptions" id="descriptions" rows="7" placeholder="Ceritakan apa yang membuat tempat ini spesial..." class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl" required></textarea>
        </div>

        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Rentang Harga Tiket Masuk</label>
          <div class="flex gap-2.5 items-center w-full">
            <input v-model="formData.entrance_ticket_min" type="number" placeholder="Rp 75.000" class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full" />
            <Subtract class="min-w-2" />
            <input v-model="formData.entrance_ticket_max" type="number" placeholder="Rp 120.000" class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full" />
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Kontak</h3>
          <label class="font-semibold">Nomor Telepon</label>
          <input v-model="formData.phone_number" type="text" placeholder="cth: +62 812 3456 7890" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
          <label class="font-semibold mt-1">Email</label>
          <input v-model="formData.email" type="email" placeholder="cth: info@spot.com" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
      </div>

      <div class="w-full md:w-3/4 lg:w-full flex flex-col gap-6">
        
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Pilih Lokasi di Peta</label>
          <p class="text-sm text-neu-700">Klik pada peta untuk menetapkan koordinat Latitude & Longitude secara otomatis.</p>
          <div class="w-full h-80 xl:h-[400px] rounded-3xl overflow-hidden border">
            <l-map v-model:zoom="zoom" :center="mapCenter" @click="handleMapClick" style="height: 100%; width: 100%">
              <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
                attribution="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
              ></l-tile-layer>
              <l-marker v-if="markerLatLng" :lat-lng="markerLatLng" :icon="defaultIcon"></l-marker>
            </l-map>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label for="street" class="text-base md:text-lg font-semibold">Jalan</label>
          <input v-model="formData.street" type="text" id="street" placeholder="cth: Jalan Pantai Kuta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
        <div class="flex flex-col gap-3">
          <label for="sub-district" class="text-base md:text-lg font-semibold">Kecamatan</label>
          <input v-model="formData.sub_district" type="text" id="sub-district" placeholder="cth: Kuta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>
        <div class="flex flex-col gap-3">
          <label for="regency" class="text-base md:text-lg font-semibold">Kabupaten</label>
          <input v-model="formData.regency" type="text" id="regency" placeholder="cth: Badung" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Koordinat</h3>
          <div class="flex gap-6">
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Latitude</label>
              <input v-model="formData.latitude" type="text" placeholder="Akan terisi otomatis dari peta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
            </div>
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Longitude</label>
              <input v-model="formData.longitude" type="text" placeholder="Akan terisi otomatis dari peta" class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full" />
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label for="facility-select" class="text-base md:text-lg font-semibold">Fasilitas</label>
          <ul class="flex flex-wrap text-sm sm:text-base gap-3 sm:gap-4">
            <li v-for="facId in formData.selectedFacilities" :key="facId" @click="removeFacility(facId)" class="bg-[#F2F8F5] text-pr-500 gap-1 font-medium items-center px-4 py-2 rounded-full flex cursor-pointer">
              {{ getFacilityName(facId) }}
              <Exit class="size-4" />
            </li>
          </ul>
          <div class="relative w-full">
            <select id="facility-select" @change="addFacility" class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none">
              <option value="" disabled selected>Pilih fasilitas untuk ditambahkan</option>
              <option v-for="fac in facilityStore.allFacilities" :key="fac.id" :value="fac.id">{{ fac.name }}</option>
            </select>
            <ArrowDown class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400" />
          </div>
        </div>

        <div class="flex flex-col gap-3">
            <label class="text-base md:text-lg font-semibold">Foto</label>
            <p class="text-sm text-neu-700">Unggah minimal {{ minPhotosRequired }} gambar untuk destinasi.</p>
            <div class="w-full">
                <label for="photo-upload" class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition">
                <Photo class="mb-1" />
                <p class="text-pr-500 font-medium text-sm mb-[2px]">Klik untuk menambah foto</p>
                <p class="text-neu-900 text-sm">atau seret & letakkan</p>
                <input id="photo-upload" type="file" class="hidden" multiple @change="handleFileChange" accept="image/*" />
                </label>
            </div>
            <div v-if="uploadedImageUrls.length > 0" class="mt-6">
                <h3 class="text-base md:text-lg font-semibold">Galeri Saat Ini ({{ uploadedImageUrls.length }} gambar)</h3>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4">
                <div v-for="(imageUrl, index) in uploadedImageUrls" :key="index" class="relative group">
                    <img :src="imageUrl" alt="Foto yang diunggah" class="w-full h-28 object-cover rounded-lg shadow-md" />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-300 flex items-center justify-center">
                    <button type="button" class="px-3 py-1 bg-red-600 text-white text-xs font-bold rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" @click="removePhoto(index)">Hapus</button>
                    </div>
                </div>
                </div>
            </div>
             <div v-else class="mt-2 text-sm text-gray-500">
                Anda perlu mengunggah minimal {{ minPhotosRequired }} gambar.
            </div>
        </div>

        <button
          type="submit"
          :disabled="isLoading || formData.photos.length < minPhotosRequired"
          class="bg-pr-500 text-neu-50 px-6 text-base sm:text-lg py-4 font-medium rounded-full hover:bg-pr-600 disabled:bg-neu-300 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Mengirim...' : 'Sarankan Tempat Ini' }}
        </button>
      </div>
    </form>
  </div>
</template>
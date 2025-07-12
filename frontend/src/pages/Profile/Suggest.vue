<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useSuggestionStore } from '@/stores/suggestionStore';
import Sidebar from '@/components/Sidebar.vue';
import Location from '@/components/icons/Location.vue';

const authStore = useAuthStore();
const suggestionStore = useSuggestionStore();

// Fungsi untuk mendapatkan gambar pertama dari sebuah suggestion
const getFirstImageUrl = (suggestion) => {
  if (suggestion.photos && suggestion.photos.length > 0) {
    return suggestion.photos[0].image;
  }
  return 'https://placehold.co/600x400?text=No+Image';
};

// Fungsi untuk menentukan kelas CSS berdasarkan status suggestion
const getStatusClass = (status) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Ambil data saat komponen pertama kali dimuat
onMounted(() => {
  suggestionStore.fetchMySuggestions();
});
</script>

<template>
  <div
    v-if="authStore.isAuthenticated && authStore.currentUser"
    class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30"
  >
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4 w-full">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Suggest History</h1>
        
        <div v-if="suggestionStore.isLoading" class="text-center py-10">
          <p>Memuat riwayat saran Anda...</p>
        </div>

        <div v-else-if="suggestionStore.error" class="text-center py-10 text-red-500">
          <p>Gagal memuat data. Silakan coba lagi nanti.</p>
        </div>
        
        <div v-else-if="suggestionStore.allMySuggestions.length > 0" class="flex gap-5 flex-wrap">
          <div
            v-for="suggestion in suggestionStore.allMySuggestions"
            :key="suggestion.id"
            class="flex flex-col border w-full sm:w-84 lg:w-72 cursor-pointer hover:scale-102 transition-all duration-500 ease-in-out border-neu-100 rounded-3xl gap-3 p-3"
          >
            <div class="relative h-43 w-full">
              <img
                :src="getFirstImageUrl(suggestion)"
                :alt="suggestion.name"
                class="object-cover w-full h-full rounded-2xl transition-transform duration-500 ease-in-out"
              />
              <div class="flex flex-col justify-between absolute inset-0 items-end p-3">
                <div
                  :class="getStatusClass(suggestion.status)"
                  class="px-4 py-2.5 flex items-center w-fit h-fit justify-center font-medium text-sm rounded-full"
                >
                  {{ suggestion.status }}
                </div>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base text-neu-900 font-semibold">{{ suggestion.name }}</h3>
              <div class="gap-1 font-medium text-sm items-center mt-1 flex">
                <Location class="size-4.5" />
                <span v-if="suggestion.sub_district || suggestion.regency">
                  {{ suggestion.sub_district }}, {{ suggestion.regency }}
                </span>
              </div>
              <p class="text-sm text-neu-600 mt-3 line-clamp-2">
                {{ suggestion.descriptions }}
              </p>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-10 text-gray-500">
          <p>Anda belum pernah menyarankan tempat apapun.</p>
        </div>

      </div>
    </main>
  </div>
</template>
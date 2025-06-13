<script setup>
import mainImage from '@/assets/images/tirta-empul-temple.webp'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2 from '@/components/icons/ArrowRight2.vue'
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import BigBali from '@/components/icons/BigBali.vue'
import Heart from '@/components/icons/Heart.vue'
import Location from '@/components/icons/Location.vue'
import Penjor from '@/components/icons/Penjor.vue'
import Search from '@/components/icons/Search.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import { ref, computed, onMounted } from 'vue'

const regenciesData = {
  badung: {
    name: 'Badung',
    description:
      'Badung Regency is largely identified with popular beach destinations like Kuta, Seminyak, and Canggu, as well as upscale areas and vibrant nightlife. It is the center of tourism in Bali.',
    topPlaces: ['Kuta Beach', 'Uluwatu Temple', 'Garuda Wisnu Kencana (GWK)'],
  },
  denpasar: {
    name: 'Denpasar',
    description:
      'Denpasar is the capital city of Bali, acting as the main hub for government, business, and education. It offers a more local, urban experience away from the main tourist strips.',
    topPlaces: ['Bajra Sandhi Monument', 'Bali Museum', 'Badung Market'],
  },
  gianyar: {
    name: 'Gianyar',
    description:
      'Known as the cultural heart of Bali, Gianyar is home to Ubud, famous for its arts, crafts, traditional dances, wellness retreats, and lush rice paddies.',
    topPlaces: ['Ubud Monkey Forest', 'Tegalalang Rice Terrace', 'Tirta Empul Temple'],
  },
  tabanan: {
    name: 'Tabanan',
    description:
      'Often called the "rice bowl" of Bali, Tabanan boasts vast, scenic rice fields, including the UNESCO World Heritage site of Jatiluwih. It offers a more serene and natural atmosphere.',
    topPlaces: ['Tanah Lot Temple', 'Jatiluwih Rice Terraces', 'Ulun Danu Beratan Temple'],
  },
  jembrana: {
    name: 'Jembrana',
    description:
      'Located in the far west of Bali, Jembrana is known for its unique traditions like the "Mekepung" buffalo races. It offers a glimpse into a more rural and less-touristy side of the island.',
    topPlaces: ['Mekepung Buffalo Races', 'Rambut Siwi Temple', 'Bunut Bolong'],
  },
  buleleng: {
    name: 'Buleleng',
    description:
      'Covering the northern coast, Buleleng is famous for the black sand beaches of Lovina, dolphin watching tours, and an abundance of stunning waterfalls hidden in its lush highlands.',
    topPlaces: ['Lovina Beach (Dolphin Watching)', 'Gitgit Waterfall', 'Sekumpul Waterfall'],
  },
  bangli: {
    name: 'Bangli',
    description:
      'As the only landlocked regency in Bali, Bangli is characterized by its dramatic volcanic landscape. It is home to the majestic Kintamani caldera, with Mount Batur and its crater lake.',
    topPlaces: ['Kintamani (Mount Batur View)', 'Penglipuran Village', 'Tukad Cepung Waterfall'],
  },
  klungkung: {
    name: 'Klungkung',
    description:
      'While the smallest regency on the mainland, Klungkung includes the famous Nusa Islands (Penida, Lembongan, and Ceningan), known for their dramatic cliffs and world-class diving spots.',
    topPlaces: [
      'Kelingking Beach (Nusa Penida)',
      "Devil's Tear (Nusa Lembongan)",
      'Kerta Gosa Pavilion',
    ],
  },
  karangasem: {
    name: 'Karangasem',
    description:
      'The easternmost regency, Karangasem is dominated by the sacred Mount Agung. It is rich in history and spirituality, featuring the "Mother Temple" Besakih and beautiful water palaces.',
    topPlaces: [
      'Besakih Temple',
      'Tirta Gangga Water Palace',
      'Lempuyang Temple (Gates of Heaven)',
    ],
  },
}

// --- State untuk interaktivitas ---
const clickedRegencyId = ref('null') // Default ke 'badung'
const tooltipText = ref('')
const tooltipVisible = ref(false)
const tooltipX = ref(0)
const tooltipY = ref(0)

const isLoadingLocation = ref(true) // State untuk menampilkan loading
const errorMessage = ref('') // Untuk menampilkan pesan error

// --- Computed property untuk menampilkan data aktif ---
const activeRegency = computed(() => {
  // Jika tidak ada yang diklik, tampilkan data default (Badung)
  const defaultId = 'badung'
  return regenciesData[clickedRegencyId.value] || regenciesData[defaultId]
})

// --- Jalankan deteksi lokasi saat komponen dimuat ---
onMounted(() => {
  fetchUserRegency()
})

// --- Fungsi Utama untuk Mendapatkan Lokasi dan Regency ---
async function fetchUserRegency() {
  isLoadingLocation.value = true
  errorMessage.value = ''

  // 1. Cek apakah browser mendukung Geolocation API
  if (!navigator.geolocation) {
    errorMessage.value = 'Geolocation is not supported by your browser.'
    clickedRegencyId.value = 'badung' // Fallback ke default
    isLoadingLocation.value = false
    return
  }

  // 2. Minta koordinat pengguna
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords

      try {
        // 3. Panggil API Nominatim untuk Reverse Geocoding
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`,
        )

        if (!response.ok) throw new Error('Failed to fetch location name.')

        const data = await response.json()

        // 4. Ekstrak nama kabupaten dari respons API
        // Nama kabupaten biasanya ada di 'state_district' atau 'county'
        const regencyName = data.address?.district || ''
        console.log(regencyName)

        // 5. Cocokkan nama dari API dengan ID di data kita
        if (regencyName) {
          // Normalisasi: "Kabupaten Badung" -> "badung"
          const detectedId = regencyName.toLowerCase().replace('kabupaten ', '')

          // Cek apakah ID yang terdeteksi ada di data kita
          if (regenciesData[detectedId]) {
            clickedRegencyId.value = detectedId
          } else {
            // Pengguna tidak berada di salah satu kabupaten Bali
            errorMessage.value = 'Location is outside of Bali. Showing default.'
            clickedRegencyId.value = 'badung' // Fallback
          }
        } else {
          // API tidak mengembalikan nama kabupaten
          errorMessage.value = 'Could not determine regency. Showing default.'
          clickedRegencyId.value = 'badung' // Fallback
        }
      } catch (error) {
        console.error('Reverse geocoding error:', error)
        errorMessage.value = 'Could not get location details.'
        clickedRegencyId.value = 'badung' // Fallback
      } finally {
        isLoadingLocation.value = false
      }
    },
    (error) => {
      // Handle error jika pengguna menolak izin atau terjadi error lain
      console.error('Geolocation error:', error.message)
      if (error.code === 1) {
        // User denied permission
        errorMessage.value = 'Location access denied. Showing default map.'
      } else {
        errorMessage.value = 'Unable to retrieve your location.'
      }
      clickedRegencyId.value = 'badung' // Fallback ke default
      isLoadingLocation.value = false
    },
  )
}

// --- Event Handlers ---
function handleRegencyHover(regency) {
  // 'regency' adalah object { id: 'badung', name: 'Badung' } dari event
  tooltipText.value = regency.name
  tooltipVisible.value = true
}

function handleRegencyClick(regency) {
  clickedRegencyId.value = regency.id
}

function handleRegencyLeave() {
  tooltipVisible.value = false
  // Kita biarkan clickedRegencyId tetap agar deskripsi tidak hilang saat kursor keluar
}

function updateTooltipPosition(event) {
  // event adalah mouse event asli
  // Kita tambahkan sedikit offset agar tooltip tidak pas di bawah kursor
  tooltipX.value = event.clientX + 15
  tooltipY.value = event.clientY + 15
}
</script>

<template>
  <!-- Hero Section -->
  <div
    class="hidden lg:flex justify-between absolute -z-50 items-center right-0 left-0 top-40 xl:top-32"
  >
    <Penjor class="w-28 xl:w-[132px]" />
    <Penjor class="transform w-28 xl:w-[132px] scale-x-[-1]" />
  </div>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30 z-50">
    <main class="flex-col flex items-center gap-8 mt-10 md:mt-16">
      <div class="flex flex-col gap-3 text-center items-center">
        <h1
          class="text-[40px] md:text-[48px] max-w-190 font-semibold leading-14 md:leading-[62px] font-se"
        >
          Discover Bali’s Icons and <span class="text-pr-500">Hidden Gems</span> in One Place
        </h1>
        <p class="text-neu-600 w-full md:max-w-[644px] text-sm md:text-base">
          Start your journey through Bali’s most loved and lesser-known destinations, all curated
          just for you.
        </p>
      </div>
      <form
        class="max-w-[640px] w-full flex items-center justify-between rounded-full outline outline-neu-200 p-1.5"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search />
          <input
            type="text"
            class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Search Destionations..."
          />
        </div>
        <button
          type="submit"
          class="px-6 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
        >
          Search
        </button>
      </form>
      <div class="relative overflow-hidden w-full h-56 md:h-64 lg:h-[380px] rounded-3xl">
        <img :src="mainImage" alt="" class="object-cover w-full h-full" />
        <div class="flex flex-col justify-between absolute bottom-0 top-0 left-0 p-4 md:p-6">
          <div
            class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
          >
            Tirta Empul Temple
            <ArrowUpRight class="size-4" />
          </div>
          <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
        </div>
      </div>
    </main>
    <!-- Exploration Section -->
    <section class="mt-24 md:mt-30 flex-col flex gap-3">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Explore
      </div>
      <div class="flex flex-col lg:flex-row sm:justify-between items-start">
        <h1
          class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] max-w-[590px] font-se"
        >
          Begin Your <span class="text-pr-500">Exploration</span> Here
        </h1>
        <div
          class="flex gap-2 w-full justify-between lg:justify-end lg:w-fit md:gap-4 mt-3 items-center"
        >
          <p class="text-neu-600 text-sm md:text-base max-w-full lg:max-w-80 lg:text-end">
            Begin your exploration of incredible destinations, from serene beaches to majestic
            mountains.
          </p>
          <div class="p-4 flex items-center w-fit h-fit justify-center bg-pr-500 rounded-full">
            <ArrowUpRight class="size-5 sm:size-6 lg:size-9 text-neu-50" />
          </div>
        </div>
      </div>
      <div class="mt-5">
        <div class="flex flex-col gap-8">
          <div class="flex flex-col xl:flex-row gap-8">
            <div v-for="i in 2" :key="i" class="flex gap-3 sm:gap-5 items-center w-full">
              <div class="relative overflow-hidden size-32 xs:size-36 md:size-45 rounded-3xl">
                <img
                  src="@/assets/images/tirta-empul-temple.webp"
                  alt="Tirta Empul"
                  class="object-cover w-full h-full"
                />
                <div
                  class="flex flex-col justify-between items-end absolute bottom-0 top-0 left-0 right-0 p-3"
                >
                  <div class="p-2 flex items-center justify-center bg-sur-50 rounded-full w-fit">
                    <Heart class="size-6 text-neu-900" />
                  </div>
                  <p class="text-[8px] w-full text-start md:text-[10px] text-neu-50">
                    Photo by unsplash
                  </p>
                </div>
              </div>

              <div class="flex flex-col flex-1">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold text-base md:text-lg line-clamp-1">
                      Tirta Empul Temple
                    </h3>
                    <div class="gap-1 md:mt-1 font-medium text-xs md:text-sm items-center flex">
                      <Location class="size-4 md:size-4.5" /><span class="line-clamp-1"
                        >Tampaksiring, Gianyar</span
                      >
                    </div>
                  </div>
                  <div
                    class="py-1 px-2 sm:px-2.5 flex items-center border border-neu-200 justify-center w-fit h-fit font-medium text-xs sm:text-sm gap-1 bg-sur-50 rounded-full"
                  >
                    <StarFilled class="size-4 md:size-4.5" />
                    4.8
                  </div>
                </div>

                <p class="text-xs md:text-sm text-neu-600 mt-2 md:mt-3 line-clamp-2">
                  Tirta Empul is a sacred temple in Bali with natural spring water baths, believed
                  to have purifying and spiritual benefits.
                </p>

                <button
                  type="button"
                  class="px-6 py-2 mt-3 md:mt-6 flex gap-2 w-fit items-center justify-center text-xs md:text-sm font-medium bg-pr-500 rounded-full text-neu-50"
                >
                  View More
                </button>
              </div>
            </div>
          </div>
          <div class="hidden xl:block mx-auto w-3/4 h-[1px] bg-neu-100"></div>
          <div class="flex flex-col xl:flex-row gap-8">
            <div v-for="i in 2" :key="i" class="flex gap-3 sm:gap-5 items-center w-full">
              <div class="relative overflow-hidden size-32 xs:size-36 md:size-45 rounded-3xl">
                <img
                  src="@/assets/images/tirta-empul-temple.webp"
                  alt="Tirta Empul"
                  class="object-cover w-full h-full"
                />
                <div
                  class="flex flex-col justify-between items-end absolute bottom-0 top-0 left-0 right-0 p-3"
                >
                  <div class="p-2 flex items-center justify-center bg-sur-50 rounded-full w-fit">
                    <Heart class="size-6 text-neu-900" />
                  </div>
                  <p class="text-[8px] w-full text-start md:text-[10px] text-neu-50">
                    Photo by unsplash
                  </p>
                </div>
              </div>

              <div class="flex flex-col flex-1">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold text-base md:text-lg line-clamp-1">
                      Tirta Empul Temple
                    </h3>
                    <div class="gap-1 md:mt-1 font-medium text-xs md:text-sm items-center flex">
                      <Location class="size-4 md:size-4.5" /><span class="line-clamp-1"
                        >Tampaksiring, Gianyar</span
                      >
                    </div>
                  </div>
                  <div
                    class="py-1 px-2 sm:px-2.5 flex items-center border border-neu-200 justify-center w-fit h-fit font-medium text-xs sm:text-sm gap-1 bg-sur-50 rounded-full"
                  >
                    <StarFilled class="size-4 md:size-4.5" />
                    4.8
                  </div>
                </div>

                <p class="text-xs md:text-sm text-neu-600 mt-2 md:mt-3 line-clamp-2">
                  Tirta Empul is a sacred temple in Bali with natural spring water baths, believed
                  to have purifying and spiritual benefits.
                </p>

                <button
                  type="button"
                  class="px-6 py-2 mt-3 md:mt-6 flex gap-2 w-fit items-center justify-center text-xs md:text-sm font-medium bg-pr-500 rounded-full text-neu-50"
                >
                  View More
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- Regency Section -->
    <section class="mt-24 md:mt-30 flex-col flex gap-3">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Regency
      </div>
      <div class="flex flex-col lg:flex-row sm:justify-between items-start">
        <h1
          class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] max-w-[590px] font-se"
        >
          Uncover the Wonders of Every Bali <span class="text-pr-500">Regency</span>
        </h1>
        <div
          class="flex gap-2 w-full justify-between lg:justify-end lg:w-fit md:gap-4 mt-3 items-center"
        >
          <p class="text-neu-600 text-sm md:text-base max-w-full lg:max-w-80 lg:text-end">
            Explore local favorites and hidden treasures waiting to be discovered in every Bali
            district.
          </p>
          <div class="p-4 flex items-center w-fit h-fit justify-center bg-pr-500 rounded-full">
            <ArrowUpRight class="size-5 sm:size-6 lg:size-9 text-neu-50" />
          </div>
        </div>
      </div>
      <div
        v-if="tooltipVisible"
        :style="{ top: `${tooltipY}px`, left: `${tooltipX}px` }"
        class="fixed z-50 rounded-md bg-neu-900 px-3 py-1.5 text-sm text-white shadow-lg pointer-events-none transition-opacity duration-200"
      >
        {{ tooltipText }}
      </div>
      <div class="mt-5">
        <div class="flex gap-10 items-center lg:items-start flex-col lg:flex-row">
          <div class="flex flex-col flex-1 order-2 lg:order-1">
            <h3 class="text-xl sm:text-2xl font-semibold mb-2">{{ activeRegency.name }}</h3>
            <p class="text-sm sm:text-base text-neu-600 mb-4">
              {{ activeRegency.description }}
            </p>
            <h3 class="text-base sm:text-lg mb-2 font-semibold">Top Places to Visit</h3>
            <ul class="flex ml-3 flex-col text-sm sm:text-base gap-2 mb-6">
              <li
                v-for="place in activeRegency.topPlaces"
                :key="place"
                class="flex gap-2 items-center"
              >
                <ArrowRight class="size-4" />{{ place }}
              </li>
            </ul>

            <button
              type="button"
              class="px-6 py-2 flex gap-2 w-fit items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
            >
              View More Destinations
            </button>
          </div>
          <BigBali
            :clicked-id="clickedRegencyId"
            @regency-hover="handleRegencyHover"
            @regency-click="handleRegencyClick"
            @regency-leave="handleRegencyLeave"
            @map-mousemove="updateTooltipPosition"
            class="w-full sm:w-3/4 lg:w-120 xl:w-[648px] order-1 lg:order-2"
          />
        </div>
      </div>
    </section>

    <!-- Mountains Section -->
    <section class="mt-24 sm:mt-30">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Mountain
      </div>

      <div class="flex flex-col mt-3">
        <h2 class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] font-se">
          Bali's <span class="text-pr-500">Majestic Peaks</span> Await
        </h2>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <p class="text-neu-600 text-sm max-w-[746px] sm:text-base mt-3">
            Embark on an unforgettable journey to Bali's majestic mountains, where breathtaking
            panoramic views and serene natural beauty await every explorer.
          </p>
          <div
            class="cursor-pointer w-fit whitespace-nowrap flex px-5.5 py-2 gap-1 items-center justify-center text-sm sm:text-base font-medium bg-pr-500 rounded-full text-white"
          >
            View All
            <ArrowRight2 class="min-w-6" />
          </div>
        </div>
      </div>

      <div class="flex gap-6 mt-8 w-fit">
        <div v-for="i in 4" :key="i" class="overflow-hidden w-80 sm:w-[340px] h-fit group">
          <div class="relative h-fit w-full">
            <img
              src="@/assets/images/mount-agung.webp"
              alt="Ubud Village"
              class="object-cover w-full h-52 sm:h-60 rounded-3xl transition-transform duration-500 ease-in-out"
            />
            <div
              class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
            >
              <div class="flex items-center justify-between w-full">
                <div
                  class="py-1 px-2.5 flex items-center justify-center font-medium text-sm gap-1 bg-sur-50 rounded-full"
                >
                  <StarFilled class="size-4 md:size-4.5" />
                  4.8
                </div>
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="size-5 md:size-6 text-neu-900" />
                </div>
              </div>
              <div class="flex justify-between items-end w-full">
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                >
                  Mount Agung
                  <ArrowUpRight class="size-4" />
                </div>
                <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
              </div>
            </div>
          </div>
          <div class="w-full px-2 mt-2 sm:mt-4">
            <h3 class="text-base sm:text-lg leading-7 text-neu-900 font-semibold">Mount Agung</h3>
            <p class="text-sm sm:text-base text-neu-600 mt-1 line-clamp-2 whitespace-normal">
              Mount Agung is Bali's highest and most sacred mountain, presenting a challenging trek
              with stunning vistas and significant spiritual importance to the Balinese people.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Hidden Gem Submission -->
    <section class="mt-24 md:mt-30">
      <div class="flex flex-col xl:flex-row gap-8 w-full items-start xl:items-center">
        <div class="flex-1 flex-col items-start flex">
          <div
            class="px-4 text-pr-500 py-2 text-sm sm:text-base flex gap-2 w-fit items-center justify-center font-medium outline-pr-500 outline rounded-full"
          >
            Hidden Gem
          </div>
          <h1
            class="text-[32px] md:text-[48px] mt-3 font-semibold leading-12 md:leading-18 font-se"
          >
            Is Balinara <span class="text-pr-500">missing</span> a place?
          </h1>
          <p class="mt-3 text-neu-600 text-sm md:text-base w-full lg:max-w-[560px] xl:w-full">
            Share your hidden Bali treasures! Help us uncover amazing off-the-beaten-path
            destinations for everyone to explore.
          </p>
          <button
            type="button"
            class="px-6 py-2 mt-6 flex text-sm md:text-base items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Let's Share
          </button>
        </div>
        <div class="relative hidden xl:block w-[600px] h-[504px]">
          <div
            class="absolute z-10 top-0 left-0 border-10 border-neu-50 overflow-hidden w-80 h-95 rounded-4xl"
          >
            <div class="relative w-full h-full">
              <img
                src="@/assets/images/monkey-forest.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full"
              />
              <div
                class="flex flex-col justify-between absolute bottom-0 right-0 top-0 left-0 p-4 md:p-6"
              >
                <div class="flex justify-between flex-1 flex-col">
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
                  >
                    Monkey Forest
                    <ArrowUpRight class="size-4" />
                  </div>
                  <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
            </div>
          </div>
          <div
            class="absolute bottom-0 right-0 overflow-hidden border-10 border-neu-50 w-80 h-95 rounded-4xl"
          >
            <div class="relative w-full h-full">
              <img
                src="@/assets/images/monkey-forest.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full"
              />
              <div
                class="flex flex-col justify-between absolute bottom-0 right-0 top-0 left-0 p-4 md:p-6"
              >
                <div class="flex justify-between flex-1 flex-col">
                  <p class="text-[8px] flex-1 text-end md:text-[10px] text-neu-50">
                    Photo by unsplash
                  </p>
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
                  >
                    Monkey Forest
                    <ArrowUpRight class="size-4" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Location from '@/components/icons/Location.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px]">
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Suggest</h1>
        <div class="flex gap-5 flex-wrap">
          <div
            class="flex flex-col border w-full sm:w-84 lg:w-72 cursor-pointer hover:scale-102 transition-all duration-500 ease-in-out border-neu-100 rounded-3xl gap-3 p-3"
          >
            <div class="relative h-43 w-full">
              <img
                src="@/assets/images/sekumpul-waterfall.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-2xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center font-medium text-sm bg-sur-50 rounded-full transition-all duration-500 ease-in-out text-[#FDB528]"
                >
                  Pending
                </div>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base text-neu-900 font-semibold">Sekumpul Waterfall</h3>
              <div class="gap-1 font-medium text-sm items-center mt-1 flex">
                <Location class="size-4.5" />Sawan, Buleleng
              </div>
              <p class="text-sm text-neu-600 mt-3 line-clamp-2">
                Sekumpul Waterfall is a stunning natural hidden gem located in the northern part of
                Bali. Situated in Sekumpul Village, Sawan District, Buleleng Regency, this
                breathtaking site features not just one, but a series of seven distinct waterfalls
                cascading down lush, verdant cliffs. The journey to witness the main waterfall
                involves an adventurous trek down pathways, crossing small rivers, and immersing
                yourself in the pristine natural surroundings. The powerful roar of the water and
                the vibrant greenery create a serene and refreshing atmosphere, offering a tranquil
                escape from the more crowded tourist spots in Bali.
              </p>
            </div>
          </div>
          <div
            class="flex flex-col border w-full sm:w-84 lg:w-72 cursor-pointer hover:scale-102 transition-all duration-500 ease-in-out border-neu-100 rounded-3xl gap-3 p-3"
          >
            <div class="relative h-43 w-full">
              <img
                src="@/assets/images/pinggan-village.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-2xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center font-medium text-sm bg-sur-50 rounded-full transition-all duration-500 ease-in-out text-[#139D31]"
                >
                  Approved
                </div>
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base text-neu-900 font-semibold">Pinggan Village</h3>
              <div class="gap-1 font-medium text-sm items-center mt-1 flex">
                <Location class="size-4.5" />Kintamani, Bangli
              </div>
              <p class="text-sm text-neu-600 mt-3 line-clamp-2">
                Pinggan Village offers extraordinary natural scenery, especially at sunrise. Located
                in the highlands of Kintamani, this village is surrounded by lush green hills often
                enveloped in a thin layer of mist in the early morning. Distant views of Mount Batur
                and Lake Batur further enhance the picturesque landscape of this village. The
                atmosphere in Pinggan Village is very peaceful and serene, far from the tourist
                crowds, making it a perfect place to enjoy the authentic natural beauty of Bali. You
                can witness local agricultural activities and experience the true Balinese rural
                life.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

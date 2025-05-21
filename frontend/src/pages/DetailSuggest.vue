<script setup lang="ts">
import Footer from '@/components/Footer.vue'
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowLeft from '@/components/icons/ArrowLeft.vue'
import Exit from '@/components/icons/Exit.vue'
import Subtract from '@/components/icons/Subtract.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <div class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <!-- Sidebar -->
      <Sidebar />

      <div class="p-0 lg:p-4 flex-1">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">
          Suggest Detail
        </h1>
        <form class="flex flex-col gap-6">
          <div class="flex flex-col sm:flex-row w-full gap-4">
            <div class="flex w-full sm:w-1/2 flex-col gap-3">
              <label for="name" class="text-base md:text-lg font-semibold">Name</label>
              <input
                type="text"
                id="name"
                value="Sekumpul Waterfall"
                placeholder="e.g., Hidden Gem Beach Club"
                class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
            <div class="flex w-full sm:w-1/2 flex-col gap-3">
              <label for="category" class="text-base md:text-lg font-semibold">Category</label>
              <div class="relative w-full">
                <select
                  id="category"
                  class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none"
                >
                  <option value="" disabled selected hidden>
                    Select a category — Beach, Temple, Mountain, etc.
                  </option>
                  <option value="beach">Beach</option>
                  <option value="temple">Temple</option>
                  <option value="mountain">Mountain</option>
                  <option value="waterfall" selected>Waterfall</option>
                </select>
                <ArrowDown
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
                />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <label for="descriptions" class="text-base md:text-lg font-semibold"
              >Descriptions</label
            >
            <textarea
              id="descriptions"
              rows="7"
              placeholder="Tell us what makes this place special..."
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
            >
Sekumpul Waterfall is a stunning natural hidden gem located in the northern part of Bali. Situated in Sekumpul Village, Sawan District, Buleleng Regency, this breathtaking site features not just one, but a series of seven distinct waterfalls cascading down lush, verdant cliffs. The journey to witness the main waterfall involves an adventurous trek down pathways, crossing small rivers, and immersing yourself in the pristine natural surroundings. The powerful roar of the water and the vibrant greenery create a serene and refreshing atmosphere, offering a tranquil escape from the more crowded tourist spots in Bali.</textarea
            >
          </div>

          <div class="flex flex-col gap-3">
            <label class="text-base md:text-lg font-semibold">Entrance Ticket</label>
            <div class="flex gap-2.5 items-center w-full">
              <input
                type="text"
                placeholder="Rp 75.000"
                value="Rp 75.000"
                class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
              <Subtract class="min-w-2" />
              <input
                type="text"
                placeholder="Rp 120.000"
                value="Rp 120.000"
                class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <label for="category" class="text-base md:text-lg font-semibold">Facilities</label>
            <ul class="flex flex-wrap text-sm sm:text-base gap-3 sm:gap-4">
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-1 font-medium items-center px-4 py-2 rounded-full flex"
              >
                Parking Area<Exit class="size-4" />
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-1 font-medium items-center px-4 py-2 rounded-full flex"
              >
                Restrooms<Exit class="size-4" />
              </li>
            </ul>
            <div class="relative w-full">
              <select
                id="category"
                class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none"
              >
                <option value="" disabled selected hidden>Select a facility option</option>
                <option value="parking-area">Parking Area</option>
                <option value="restrooms">Restrooms</option>
              </select>
              <ArrowDown
                class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
              />
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <h3 class="text-base md:text-lg font-semibold">Contact</h3>
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="flex-col w-full sm:w-1/2 flex gap-3">
                <label class="font-semibold">Phone Number</label>
                <input
                  type="text"
                  placeholder="e.g., +62 812 3456 7890"
                  value="0812345678991"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex-col w-full sm:w-1/2 flex gap-3">
                <label class="font-semibold mt-1">Mail</label>
                <input
                  type="text"
                  placeholder="e.g., info@spot.com"
                  value="sekumpul@info.com"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-col w-full sm:w-1/2 order-2 sm:order-1 flex gap-4">
              <div class="flex flex-col gap-3">
                <label class="font-semibold">Street</label>
                <input
                  type="text"
                  placeholder="e.g., Jalan Pantai Kuta"
                  value="Jalan Air Terjun Desa Sekumpul"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="name" class="text-base md:text-lg font-semibold">Sub-district</label>
                <input
                  type="text"
                  id="name"
                  placeholder="e.g., Kuta"
                  value="Sawan"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="name" class="text-base md:text-lg font-semibold">Regency</label>
                <input
                  type="text"
                  id="name"
                  placeholder="e.g., Badung"
                  value="Buleleng"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
            </div>
            <div class="flex-col w-full sm:w-1/2 order-1 sm:order-2 flex gap-3">
              <label class="text-base md:text-lg font-semibold">Map Location</label>
              <div class="w-full h-80 sm:h-full rounded-2xl overflow-hidden">
                <iframe
                  class="w-full h-full"
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <h3 class="text-base md:text-lg font-semibold">Coordinate</h3>
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="flex flex-col gap-3 w-full sm:w-1/2">
                <label class="font-semibold mt-1">Latitude</label>
                <input
                  type="text"
                  placeholder="e.g., -8.709201"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3 w-full sm:w-1/2">
                <label class="font-semibold mt-1">Longitude</label>
                <input
                  type="text"
                  placeholder="e.g., 115.168263"
                  class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3 w-full sm:w-1/2">
            <label for="name" class="text-base md:text-lg font-semibold">Add Photos</label>
            <img src="@/assets/images/sekumpul-waterfall.webp" alt="" class="rounded-2xl" />
            <!-- <div class="w-full">
              <label
                for="photo-upload"
                class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition"
              >
                <Photo class="mb-1" />

                <p class="text-pr-500 font-medium text-sm mb-[2px]">Click to add photos</p>
                <p class="text-neu-900 text-sm">or drag & drop</p>

                <input id="photo-upload" type="file" class="hidden" multiple />
              </label>
            </div> -->
          </div>
        </form>
      </div>
      <!-- Main Content -->
    </div>
  </div>
</template>

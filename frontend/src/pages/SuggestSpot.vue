<script setup>
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Exit from '@/components/icons/Exit.vue'
import Photo from '@/components/icons/Photo.vue'
import Subtract from '@/components/icons/Subtract.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px]">
    <form class="flex flex-col lg:flex-row gap-6 lg:gap-16 mt-10 md:mt-16">
      <!-- Form Left -->
      <div class="w-full md:w-3/4 lg:min-w-80 xl:min-w-120 flex flex-col gap-6">
        <h1 class="text-4xl sm:text-[42px] font-semibold leading-12 sm:leading-[62px] font-se">
          <span class="text-pr-500">Suggest</span> a Spot and Inspire Travelers!
        </h1>
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Name</label>
          <input
            type="text"
            id="name"
            placeholder="e.g., Hidden Gem Beach Club"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
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
            </select>
            <ArrowDown
              class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
            />
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold">Descriptions</label>
          <textarea
            id="descriptions"
            rows="7"
            placeholder="Tell us what makes this place special..."
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
          ></textarea>
        </div>

        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Entrance Ticket</label>
          <div class="flex gap-2.5 items-center w-full">
            <input
              type="text"
              placeholder="Rp 75.000"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
            <Subtract class="min-w-2" />
            <input
              type="text"
              placeholder="Rp 120.000"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Contact</h3>
          <label class="font-semibold">Phone Number</label>
          <input
            type="text"
            placeholder="e.g., +62 812 3456 7890"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
          <label class="font-semibold mt-1">Mail</label>
          <input
            type="text"
            placeholder="e.g., info@spot.com"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>

        <div class="relative hidden lg:block overflow-hidden w-full h-66 rounded-3xl">
          <img
            src="@/assets/images/kuta-beach.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />

          <div
            class="flex flex-col justify-between bg-neu-900/40 absolute bottom-0 top-0 left-0 p-4 md:p-6"
          >
            <div
              class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
            >
              Kuta Beach
              <ArrowUpRight class="size-4" />
            </div>
            <div class="text-neu-50 flex gap-1 flex-col">
              <h2 class="text-xl sm:text-2xl font-semibold">Why Suggest a Spot?</h2>
              <p class="text-sm sm:text-base">
                By suggesting a spot, you help travelers uncover Bali's authentic charm, share
                hidden treasures, and support local communities to thrive.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Right -->
      <div class="w-full md:w-3/4 lg:w-full flex flex-col gap-6">
        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Map Location</label>
          <div class="w-full h-80 xl:h-[400px] rounded-3xl overflow-hidden">
            <iframe
              class="w-full h-full"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Street</label>
          <input
            type="text"
            id="name"
            placeholder="e.g., Jalan Pantai Kuta"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Sub-district</label>
          <input
            type="text"
            id="name"
            placeholder="e.g., Kuta"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base md:text-lg font-semibold">Regency</label>
          <input
            type="text"
            id="name"
            placeholder="e.g., Badung"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-base md:text-lg font-semibold">Coordinate</h3>
          <div class="flex gap-6">
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Latitude</label>
              <input
                type="text"
                placeholder="e.g., -8.709201"
                class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
            <div class="flex flex-col gap-3 w-1/2">
              <label class="font-semibold mt-1">Longitude</label>
              <input
                type="text"
                placeholder="e.g., 115.168263"
                class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
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
          <label for="name" class="text-base md:text-lg font-semibold">Add Photos</label>
          <div class="w-full">
            <label
              for="photo-upload"
              class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition"
            >
              <Photo class="mb-1" />

              <!-- Text -->
              <p class="text-pr-500 font-medium text-sm mb-[2px]">Click to add photos</p>
              <p class="text-neu-900 text-sm">or drag & drop</p>

              <!-- Hidden input -->
              <input id="photo-upload" type="file" class="hidden" multiple />
            </label>
          </div>
        </div>

        <button
          type="submit"
          class="bg-pr-200 text-neu-50 px-6 text-base sm:text-lg py-4 font-medium rounded-full"
        >
          Suggest this spot
        </button>
        <div class="relative block w-3/4 lg:hidden overflow-hidden mt-8 h-66 rounded-3xl">
          <img
            src="@/assets/images/kuta-beach.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />

          <div
            class="flex flex-col justify-between bg-neu-900/40 absolute bottom-0 top-0 left-0 p-4 md:p-6"
          >
            <div
              class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
            >
              Kuta Beach
              <ArrowUpRight class="size-4" />
            </div>
            <div class="text-neu-50 flex gap-1 flex-col">
              <h2 class="text-xl sm:text-2xl font-semibold">Why Suggest a Spot?</h2>
              <p class="text-sm sm:text-base">
                By suggesting a spot, you help travelers uncover Bali's authentic charm, share
                hidden treasures, and support local communities to thrive.
              </p>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

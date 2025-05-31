<script setup lang="ts">
import ArrowDown from '@/components/icons/ArrowDown.vue'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Exit from '@/components/icons/Exit.vue'
import Subtract from '@/components/icons/Subtract.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Detail Suggested Spot</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminSuggestions' }" class="hover:underline"
          >Suggestions</RouterLink
        >
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Detail</span>
      </div>
    </div>

    <form class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Form Left -->
      <div
        class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Name</label>
          <input
            type="text"
            id="name"
            placeholder="e.g., Hidden Gem Beach Club"
            value="Tanah Lot"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label for="travelername" class="text-base font-semibold">Traveler Name</label>
          <input
            type="text"
            id="travelername"
            placeholder="e.g., Udin Surudin"
            value="Udin Surudin"
            disabled
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col gap-3">
          <label for="category" class="text-base font-semibold">Status</label>
          <div class="relative w-full">
            <select
              id="category"
              class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none"
            >
              <option value="" selected hidden>
                Select a status — Pending, Approved, and Rejected.
              </option>
              <option value="pending" selected>Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
            <ArrowDown
              class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
            />
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="category" class="text-base font-semibold">Category</label>
          <div class="relative w-full">
            <select
              id="category"
              disabled
              class="w-full px-3 py-3 text-sm bg-[#F2F2F2] text-neu-900 border border-neu-200 rounded-full appearance-none"
            >
              <option value="" disabled selected hidden>
                Select a category — Beach, Temple, Mountain, etc.
              </option>
              <option value="beach">Beach</option>
              <option value="temple" selected>Temple</option>
              <option value="mountain">Mountain</option>
            </select>
            <ArrowDown
              class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
            />
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base font-semibold">Descriptions</label>
          <textarea
            id="descriptions"
            rows="7"
            disabled
            placeholder="Tell us what makes this place special..."
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-3xl"
          >
Tanah Lot Temple is an iconic Balinese sea temple perched dramatically on a rock formation just off the coast. This ancient Hindu shrine is dedicated to the sea gods and is renowned for its stunning ocean views, especially during sunset. The temple's name literally translates to "Land in the Sea," perfectly describing its unique offshore setting. Often regarded as one of Bali's most important landmarks, Tanah Lot not only offers breathtaking scenery but also holds deep spiritual significance for the local Balinese people.</textarea
          >
        </div>

        <div class="flex flex-col gap-3">
          <label for="category" class="text-base font-semibold">Facilities</label>
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
              disabled
              class="w-full px-3 py-3 text-sm bg-[#F2F2F2] text-neu-900 border border-neu-200 rounded-full appearance-none"
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
          <label class="text-base md:text-lg font-semibold">Entrance Ticket</label>
          <div class="flex gap-2.5 items-center w-full">
            <input
              type="text"
              placeholder="Rp 75.000"
              value="Rp 75.000"
              disabled
              class="px-3 py-3 text-sm bg-[#F2F2F2] w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
            <Subtract class="min-w-2" />
            <input
              type="text"
              placeholder="Rp 120.000"
              value="Rp 120.000"
              disabled
              class="px-3 py-3 text-sm w-full bg-[#F2F2F2] border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-base font-semibold">Contact</h3>
          <label class="text-sm font-semibold">Phone Number</label>
          <input
            type="text"
            disabled
            placeholder="e.g., +62 812 3456 7890"
            value="081234567891"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
          <label class="text-sm font-semibold mt-1">Mail</label>
          <input
            type="text"
            disabled
            placeholder="e.g., info@spot.com"
            value="tanahlot@spot.com"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>

        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Photo</label>

          <img
            src="@/assets/images/mount-agung.webp"
            alt="Ubud Village"
            class="object-cover w-[200px] h-[112px] rounded-2xl"
          />
        </div>
      </div>

      <!-- Form Right -->
      <div
        class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl"
      >
        <!-- Map -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Map Location</label>
          <div class="w-full h-62 rounded-3xl overflow-hidden">
            <iframe
              class="w-full h-full"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>

        <!-- Street -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Street</label>
          <input
            type="text"
            disabled
            placeholder="e.g., Jalan Pantai Kuta"
            value="Beraban Village"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-gray-300 rounded-full"
          />
        </div>

        <!-- Sub-district -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Sub-district</label>
          <input
            type="text"
            disabled
            placeholder="e.g., Kuta"
            value="Kediri"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-gray-300 rounded-full"
          />
        </div>

        <!-- Regency -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Regency</label>
          <input
            type="text"
            disabled
            placeholder="e.g., Badung"
            value="Tabanan"
            class="px-3 py-3 text-sm border bg-[#F2F2F2] border-gray-300 rounded-full"
          />
        </div>

        <!-- Latitude & Longitude -->
        <div class="flex flex-col gap-3">
          <h3 class="text-base font-semibold">Coordinate</h3>
          <div class="flex flex-col sm:flex-row gap-6 sm:gap-4">
            <div class="flex flex-col gap-3 w-full">
              <label class="font-semibold text-sm mt-1">Latitude</label>
              <input
                type="text"
                disabled
                placeholder="e.g., -8.709201"
                value="-8.709201"
                class="px-3 py-3 text-sm w-full border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
            <div class="flex flex-col gap-3 w-full">
              <label class="font-semibold text-sm mt-1">Longitude</label>
              <input
                type="text"
                disabled
                placeholder="e.g., 115.168263"
                value="115.168263"
                class="px-3 py-3 text-sm w-full border bg-[#F2F2F2] placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
          </div>
        </div>
      </div>
    </form>

    <div class="flex gap-2.5 items-center">
      <RouterLink
        :to="{ name: 'AdminSuggestions' }"
        type="button"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        Back
      </RouterLink>
    </div>
  </div>
</template>

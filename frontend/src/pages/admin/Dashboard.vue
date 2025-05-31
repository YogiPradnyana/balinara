<script setup lang="ts">
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import MapPin from '@/components/icons/MapPin.vue'
import Message from '@/components/icons/Message.vue'
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import Tag from '@/components/icons/Tag.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
import User from '@/components/icons/User.vue'
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Dashboard</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Master</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Dashboard</span>
      </div>
    </div>
    <div class="flex gap-3">
      <div class="flex p-4 w-full border border-neu-100 rounded-3xl">
        <div class="flex flex-col gap-2">
          <User class="size-7 text-neu-600" />
          <h3 class="font-semibold text-xl">30</h3>
          <p class="max-w-35 text-neu-600">Registered Travelers</p>
        </div>
      </div>
      <div class="flex p-4 w-full border border-neu-100 rounded-3xl">
        <div class="flex flex-col gap-2">
          <OutlinedLocation class="size-7 text-neu-600" />
          <h3 class="font-semibold text-xl">64</h3>
          <p class="max-w-35 text-neu-600">Total Destinations</p>
        </div>
      </div>
      <div class="flex p-4 w-full border border-neu-100 rounded-3xl">
        <div class="flex flex-col gap-2">
          <Tag class="size-7 text-neu-600" />
          <h3 class="font-semibold text-xl">10</h3>
          <p class="max-w-35 text-neu-600">Total Destination Categories</p>
        </div>
      </div>
      <div class="flex p-4 w-full border border-neu-100 rounded-3xl">
        <div class="flex flex-col gap-2">
          <MapPin class="size-7 text-neu-600" />
          <h3 class="font-semibold text-xl">10</h3>
          <p class="max-w-35 text-neu-600">Pending Spot Suggestions</p>
        </div>
      </div>
      <div class="flex p-4 w-full border border-neu-100 rounded-3xl">
        <div class="flex flex-col gap-2">
          <Message class="size-7 text-neu-600" />
          <h3 class="font-semibold text-2xl">10</h3>
          <p class="max-w-35 text-neu-600">Total Reviews Submitted</p>
        </div>
      </div>
    </div>
    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex p-4">
        <h2 class="font-semibold">New Suggestions</h2>
      </div>
      <div class="w-full h-[1px] bg-neu-100"></div>
      <div class="flex flex-col p-4">
        <div class="border border-neu-100 gap-2 px-2.5 py-2 flex items-center w-1/2 rounded-full">
          <Search class="size-6" />
          <input
            type="text"
            class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Search something..."
          />
        </div>

        <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">NAME SPOT</th>
                  <th class="p-4 text-start font-semibold">CATEGORY</th>
                  <th colspan="2" class="p-4 text-start font-semibold">ADDRESS</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-sm text-neu-700 border-b border-neu-100" v-for="i in 5" :key="i">
                  <td class="p-4 text-neu-900">1</td>
                  <td class="p-4 text-neu-900 font-semibold">Balangan Beach</td>
                  <td class="p-4">Beach</td>
                  <td colspan="2" class="p-4">Kec. Kuta Sel., Kabupaten Badung, Bali, Indonesia</td>
                  <td class="p-4 flex gap-3">
                    <button
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </button>
                    <button
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                    >
                      <TrashCan class="size-5 text-neu-50" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="flex justify-between gap-3 flex-wrap items-center mt-3">
          <div class="text-sm text-neu-600">
            Showing <span class="font-medium text-neu-900">1</span> to
            <span class="font-medium text-neu-900">1</span> of
            <span class="font-medium text-neu-900">10</span> Entries
          </div>
          <div class="flex items-center rounded-[8px] overflow-hidden">
            <div class="flex bg-neu-100 text-neu-300 gap-2 h-8 px-3 items-center font-semibold">
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </div>
            <div class="flex bg-neu-100 gap-2 h-8 px-3 cursor-pointer items-center font-semibold">
              Next<ArrowRight2Bold class="size-4" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

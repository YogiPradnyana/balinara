<script setup>
import mainImage from '@/assets/images/tegalallang-rice-terraces.webp'
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Location from '@/components/icons/Location.vue'
import Photo from '@/components/icons/Photo.vue'
import Search from '@/components/icons/Search.vue'
import Star from '@/components/icons/Star.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import { onBeforeUnmount, onMounted, ref } from 'vue'

const selectedRating = ref(0)
const hoverRating = ref(0)
const isSearch = ref(0)
const formRef = ref(null)
const inputRef = ref(null)

const handleClickOutside = (event) => {
  if (formRef.value && !formRef.value.contains(event.target)) {
    isSearch.value = false
  }
}

const handleFormClick = () => {
  isSearch.value = true
  inputRef.value?.focus()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <div class="relative w-full h-124 xs:h-[380px] rounded-3xl mt-10 md:mt-16">
      <img :src="mainImage" alt="" class="object-cover w-full h-full rounded-3xl overflow-hidden" />
      <div
        class="flex flex-col w-full justify-between absolute bottom-0 top-0 left-0 p-4 md:p-6 bg-neu-900/24"
      >
        <div
          class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full"
        >
          Tegalalang Rice Terraces
          <ArrowUpRight class="size-4" />
        </div>
        <div class="flex-col flex items-center gap-2.5">
          <h1
            class="text-[40px] text-neu-50 md:text-[48px] max-w-160 text-center font-semibold leading-14 md:leading-[62px] font-se"
          >
            Help Future Travelers with Your Insight
          </h1>
          <div class="max-w-[640px] relative w-full h-[52px]">
            <form
              ref="formRef"
              @click="handleFormClick"
              class="absolute w-full flex outline bg-sur-50 outline-neu-200 p-1.5"
              :class="[
                isSearch
                  ? ' rounded-3xl flex-col'
                  : 'justify-between  flex-row items-center rounded-full',
              ]"
            >
              <div
                :class="[
                  'wrapper gap-2 ps-1.5 flex items-center w-full',
                  isSearch ? 'h-[40px]' : 'h-auto',
                ]"
              >
                <Search class="min-w-5" />
                <input
                  ref="inputRef"
                  type="text"
                  class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
                  placeholder="Search Destionations..."
                />
              </div>
              <div class="w-full px-1.5" :class="[isSearch ? 'block' : 'hidden']">
                <div :class="['w-full h-[1px] bg-neu-200', isSearch ? 'block' : 'hidden']"></div>
                <div class="py-4 flex gap-4 flex-col">
                  <div
                    v-for="i in 3"
                    :key="i"
                    class="flex items-center cursor-pointer gap-3 px-3 py-1.5 transition duration-300 hover:bg-[#EFF6F2] rounded-2xl"
                  >
                    <img
                      src="@/assets/images/gitgit-waterfall.webp"
                      class="object-cover size-15 rounded-xl"
                    />
                    <div class="flex flex-col gap-1.5">
                      <h3 class="text-sm font-semibold">Gitgit Waterfall</h3>
                      <div class="flex gap-1 items-center">
                        <Location class="size-4" />
                        <p class="text-xs font-medium text-neu-600">Sukasada, Buleleng</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <button
                type="submit"
                :class="[
                  'px-6 py-2 gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50',
                  isSearch ? 'hidden' : 'flex',
                ]"
              >
                Search
              </button>
            </form>
          </div>
        </div>
        <p class="text-[8px] md:text-[10px] text-neu-50">Photo by tripadvisor</p>
      </div>
    </div>
    <!-- Review Section -->
    <section class="mt-16 md:mt-20 flex flex-col lg:flex-row gap-8 sm:gap-10 lg:gap-16">
      <!-- Left Column -->
      <div class="flex flex-col w-full lg:w-100 xl:w-112">
        <h1
          class="text-4xl sm:text-[42px] font-semibold leading-12 max-w-100 lg:w-full sm:leading-[62px] font-se mb-6"
        >
          Tell us about your
          <span class="text-pr-500">experience</span>
        </h1>
        <div class="flex flex-row lg:flex-col gap-6 lg:gap-12">
          <div
            class="flex flex-col border w-full xs:w-3/4 md:w-1/2 lg:w-full cursor-pointer border-neu-100 rounded-4xl gap-3 p-3"
          >
            <div class="relative w-full">
              <!-- <img
              src="@/assets/images/mount-agung.webp"
              alt="Ubud Village"
              class="object-cover w-full h-74 rounded-3xl"
            /> -->
              <div
                class="flex justify-center w-full h-56 lg:h-66 xl:h-74 rounded-3xl font-medium text-xl lg:text-2xl text-center bg-neu-100 items-center p-8"
              >
                First, choose your destination.
              </div>
            </div>
            <div class="flex flex-col">
              <h3 class="text-base sm:text-lg font-semibold">Title</h3>
              <div class="gap-1 font-medium items-center text-sm sm:text-base mt-1 flex">
                <Location class="size-4 sm:size-5" />Location
              </div>
              <p class="text-neu-600 mt-3 text-sm sm:text-base line-clamp-2">Descriptions</p>
            </div>
          </div>
          <div class="text-center hidden lg:block">
            <p class="text-base md:text-lg font-semibold mb-1">Can’t find the place?</p>
            <p class="text-sm sm:text-base">Tell us about it so we can improve what we show.</p>
            <button
              class="mt-3 px-6 py-2 text-sm sm:text-base font-medium border border-neu-900 rounded-full"
            >
              Suggest a Spot
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <form class="flex-1 flex-col flex gap-8">
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold"
            >Rate Your Experience</label
          >
          <div class="flex gap-2">
            <button
              v-for="i in 5"
              :key="i"
              @click="selectedRating = i"
              @mouseover="hoverRating = i"
              @mouseleave="hoverRating = 0"
              class="transition cursor-pointer"
            >
              <component
                :is="i <= (hoverRating || selectedRating) ? StarFilled : Star"
                class="size-7 lg:size-9"
                :class="i <= (hoverRating || selectedRating) ? '' : 'text-[#FDB528]'"
              />
            </button>
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base md:text-lg font-semibold"
            >Describe the Vibe in Your Words</label
          >
          <textarea
            id="descriptions"
            rows="7"
            placeholder="Clean, quiet, and perfect for relaxing. Highly recommended!"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
          ></textarea>
        </div>

        <div class="flex flex-col">
          <label for="name" class="mb-1 text-base md:text-lg font-semibold"
            >Capture the Moment? Share It!</label
          >
          <p class="text-neu-600 mb-3">Optional</p>
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

        <label class="flex items-center gap-3">
          <input type="checkbox" class="size-5" />
          I agree that my review is honest and respectful.
        </label>

        <button
          type="submit"
          class="bg-pr-200 text-neu-50 px-6 text-base sm:text-lg py-4 font-medium rounded-full"
        >
          Post My Review
        </button>

        <div class="text-center block lg:hidden mt-12">
          <p class="text-base md:text-lg font-semibold mb-1">Can’t find the place?</p>
          <p class="text-sm sm:text-base">Tell us about it so we can improve what we show.</p>
          <button
            class="mt-3 px-6 py-2 text-sm sm:text-base font-medium border border-neu-900 rounded-full"
          >
            Suggest a Spot
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

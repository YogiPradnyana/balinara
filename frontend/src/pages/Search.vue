<script setup>
import Filter from '@/components/icons/Filter.vue'
import Heart from '@/components/icons/Heart.vue'
import Location from '@/components/icons/Location.vue'
import Star from '@/components/icons/Star.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const keyword = ref(route.query.q || '')
const selectedRating = ref(0)
const hoverRating = ref(0)
const isFilterOpen = ref(0)
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] bg-[#ECF4F0] pb-24 md:pb-30">
    <div class="flex flex-col md:flex-row gap-8 pt-10 md:pt-16">
      <!-- Sidebar -->
      <div class="min-w-52 lg:min-w-60 space-y-5 lg:space-y-8 hidden md:block">
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Categories</h3>
          <ul class="space-y-1.5">
            <li>
              <label class="flex items-center gap-2">
                <input type="checkbox" value="beach" />
                Beach
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="checkbox" value="mountain" />
                Mountain
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="checkbox" value="lake" />
                Lake
              </label>
            </li>
          </ul>
        </div>
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Regency</h3>
          <ul class="space-y-1.5">
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="denpasar" />
                Denpasar
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="badung" />
                Badung
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="klungkung" />
                Klungkung
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="bangli" />
                Bangli
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="tabanan" />
                Tabanan
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="gianyar" />
                Gianyar
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="buleleng" />
                Buleleng
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="jembrana" />
                Jembrana
              </label>
            </li>
            <li>
              <label class="flex items-center gap-2">
                <input type="radio" name="regency" value="karangasem" />
                Karangasem
              </label>
            </li>
          </ul>
        </div>
        <div class="flex p-6 bg-sur-50 rounded-3xl flex-col">
          <h3 class="text-base sm:text-lg font-semibold mb-3">Rating</h3>
          <div class="flex gap-1">
            <button
              v-for="i in 5"
              :key="i"
              @click="selectedRating = i"
              @mouseover="hoverRating = i"
              @mouseleave="hoverRating = 0"
              class="text-2xl transition"
            >
              <component
                :is="i <= (hoverRating || selectedRating) ? StarFilled : Star"
                class="size-6 lg:size-8"
                :class="i <= (hoverRating || selectedRating) ? '' : 'text-[#FDB528]'"
              />
            </button>
          </div>
        </div>
      </div>

      <!-- Search Result List -->
      <div class="flex-1 flex flex-col">
        <h1 class="text-2xl md:mb-1 md:text-[32px] font-se font-semibold leading-10 md:leading-12">
          Search results for "{{ keyword }}"
        </h1>
        <p class="text-sm sm:text-base">Your adventure starts with places we found for you.</p>
        <div class="md:hidden flex relative w-full justify-end">
          <div
            @click="isFilterOpen = !isFilterOpen"
            class="flex w-fit rounded-lg mt-2 bg-sur-50 p-2 items-center justify-center"
          >
            <Filter class="size-5" />
          </div>
          <div
            class="top-13 min-w-56 p-4 absolute bg-sur-50 shadow-sm rounded-2xl flex-col gap-4"
            :class="isFilterOpen ? 'flex' : 'hidden'"
          >
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Categories</h3>
              <ul class="space-y-1.5 text-sm">
                <li>
                  <label class="flex items-center gap-1.5">
                    <input type="checkbox" value="beach" />
                    Beach
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-1.5">
                    <input type="checkbox" value="mountain" />
                    Mountain
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-1.5">
                    <input type="checkbox" value="lake" />
                    Lake
                  </label>
                </li>
              </ul>
            </div>
            <div class="w-3/4 h-[1px] bg-neu-100"></div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Regency</h3>
              <ul class="space-y-1.5 text-sm">
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="denpasar" />
                    Denpasar
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="badung" />
                    Badung
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="klungkung" />
                    Klungkung
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="bangli" />
                    Bangli
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="tabanan" />
                    Tabanan
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="gianyar" />
                    Gianyar
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="buleleng" />
                    Buleleng
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="jembrana" />
                    Jembrana
                  </label>
                </li>
                <li>
                  <label class="flex items-center gap-2">
                    <input type="radio" name="regency" value="karangasem" />
                    Karangasem
                  </label>
                </li>
              </ul>
            </div>
            <div class="w-3/4 h-[1px] bg-neu-100"></div>
            <div class="flex flex-col">
              <h3 class="font-semibold mb-2">Rating</h3>
              <div class="flex gap-1">
                <button
                  v-for="i in 5"
                  :key="i"
                  @click="selectedRating = i"
                  @mouseover="hoverRating = i"
                  @mouseleave="hoverRating = 0"
                  class="text-2xl transition"
                >
                  <component
                    :is="i <= (hoverRating || selectedRating) ? StarFilled : Star"
                    class="size-5"
                    :class="i <= (hoverRating || selectedRating) ? '' : 'text-[#FDB528]'"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Card -->
        <ul class="flex gap-4 mt-4 md:mt-6 flex-col">
          <div
            v-for="i in 5"
            :key="i"
            class="flex bg-sur-50 rounded-4xl p-4 gap-3 sm:gap-5 items-center w-full"
          >
            <div
              class="relative overflow-hidden size-32 xs:size-36 md:size-40 lg:size-45 rounded-3xl"
            >
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

              <p class="text-sm md:text-base text-neu-600 mt-2 lg:mt-3 line-clamp-2">
                Tirta Empul is a sacred temple in Bali with natural spring water baths, believed to
                have purifying and spiritual benefits.
              </p>

              <button
                type="button"
                class="px-6 py-2 mt-3 sm:mt-4 lg:mt-6 flex gap-2 w-fit items-center justify-center text-xs md:text-sm font-medium bg-pr-500 rounded-full text-neu-50"
              >
                View More
              </button>
            </div>
          </div>
        </ul>
      </div>
    </div>
  </div>
</template>

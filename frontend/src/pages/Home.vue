<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Search from '@/components/icons/Search.vue'
import heroImage from '@/assets/images/ubud-village.webp'
import Heart from '@/components/icons/Heart.vue'
import Leaf from '@/components/icons/Leaf.vue'
import AI from '@/components/icons/AI.vue'
import Send from '@/components/icons/Send.vue'
import DoubleQuotes from '@/components/icons/DoubleQuotes.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import { useDestinationStore } from '@/stores/destinationStore'
import { ref, onMounted, onActivated, nextTick } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import WishlistButton from '@/components/WishlistButton.vue'
import { useWishlistStore } from '@/stores/wishlistStore'
import { gsap } from 'gsap'
import { Draggable } from 'gsap/Draggable'

gsap.registerPlugin(Draggable)

const containerRef = ref(null)
const proxyRef = ref(null)

const router = useRouter()
const destinationStore = useDestinationStore()

// const heroDestination = ref(null) // Untuk section hero paling atas
const populerDestinations = ref([]) // Untuk section "Begin Your Exploration"
const mountainDestinations = ref([])

const searchTerm = ref('')

function performSearch() {
  if (searchTerm.value.trim()) {
    router.push({
      name: 'Search',
      query: { search: searchTerm.value },
    })
  } else {
    router.push({
      name: 'Search',
    })
  }
}

onMounted(async () => {
  try {
    const data = await destinationStore.fetchDestinations({
      ordering: '-average_rating',
      page_size: 6,
    })

    populerDestinations.value = data

    await nextTick()

    if (proxyRef.value && containerRef.value) {
      Draggable.create(proxyRef.value, {
        type: 'x',
        bounds: containerRef.value,
        inertia: true,
        edgeResistance: 0.65,
        dragClickables: false,
      })
    }
  } catch (error) {
    console.error('Gagal saat onMounted:', error)
  }
})

onActivated(() => {
  useWishlistStore().fetchWishlist()
})
</script>

<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <main class="flex-col flex items-center gap-8 mt-10 md:mt-16">
      <div class="flex flex-col gap-3 text-center items-center">
        <h1 class="text-[40px] md:text-[48px] font-semibold leading-14 md:leading-[62px] font-se">
          Your Journey to <span class="text-pr-500">Bali</span> Starts Here
        </h1>
        <p class="text-neu-600 w-full md:max-w-[644px] text-sm md:text-base">
          From serene rice fields to lively beach clubs, explore Bali like never before. Ask our AI
          chatbot anything — your digital tour guide is always ready.
        </p>
      </div>
      <form
        @submit.prevent="performSearch"
        class="max-w-[640px] w-full flex items-center justify-between rounded-full outline outline-neu-200 p-1.5"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search />
          <input
            type="text"
            v-model="searchTerm"
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
        <img :src="heroImage" alt="Ubud Village" class="object-cover w-full h-full" />
        <div class="flex flex-col justify-between absolute bottom-0 top-0 left-0 p-4 md:p-6">
          <RouterLink
            :to="{ name: 'DetailDestination', params: { slug: 'ubud-village' } }"
            class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
          >
            Ubud Village
            <ArrowUpRight class="size-4" />
          </RouterLink>
          <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
        </div>
      </div>
    </main>

    <section class="mt-24 md:mt-30 flex-col flex gap-3">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Destinations
      </div>
      <div class="flex flex-col lg:flex-row sm:justify-between items-start">
        <h1
          class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] max-w-[590px] font-se"
        >
          Find The Best <span class="text-pr-500">Destinations</span> in Bali
        </h1>
        <div
          class="flex gap-2 w-full justify-between lg:justify-end lg:w-fit md:gap-4 mt-3 items-center"
        >
          <p class="text-neu-600 text-sm md:text-base max-w-full lg:max-w-80 lg:text-end">
            Find your perfect Bali escape — explore beaches, temples, mountains, and local treasures
            effortlessly.
          </p>
          <RouterLink
            :to="{ name: 'Search' }"
            class="p-4 flex items-center w-fit h-fit justify-center bg-pr-500 rounded-full"
          >
            <ArrowUpRight class="size-5 sm:size-6 lg:size-9 text-neu-50" />
          </RouterLink>
        </div>
      </div>
      <div ref="containerRef" class="mt-8 cursor-grab">
        <div ref="proxyRef" class="flex gap-8 w-max">
          <div
            v-for="destination in populerDestinations"
            :key="destination.id"
            class="overflow-hidden w-66 md:w-[340px] h-90 md:h-[460px] rounded-4xl group"
          >
            <div
              class="relative h-full w-full sm:group-hover:h-86 transition-all duration-500 ease-in-out"
            >
              <img
                :src="destination.primary_image_url || 'https://placehold.co/180x180'"
                :alt="destination.name"
                class="object-cover w-full h-full rounded-4xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <WishlistButton :destination-id="destination.id" :is-icon="true" />
                <div class="flex justify-between items-end w-full">
                  <RouterLink
                    :to="{ name: 'DetailDestination', params: { slug: destination.slug } }"
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                  >
                    {{ destination.name }}
                    <ArrowUpRight class="size-4" />
                  </RouterLink>
                  <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
              <div class="sm:static w-full px-2">
                <h3 class="text-lg mt-4 leading-7 text-neu-900 font-semibold">
                  {{ destination.name }}
                </h3>
                <p class="text-neu-600 mt-1 line-clamp-2 whitespace-normal">
                  {{ destination.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="mt-24 md:mt-30">
      <div
        class="flex flex-col lg:flex-row gap-6 md:gap-8 items-center p-4 md:p-8 rounded-4xl bg-se-50"
      >
        <div
          class="relative overflow-hidden w-full lg:w-7/12 h-56 sm:h-64 md:h-72 lg:h-[380px] rounded-3xl"
        >
          <img
            src="@/assets/images/jatiluwih.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div class="flex flex-col justify-between absolute bottom-0 top-0 left-0 p-6">
            <RouterLink
              :to="{ name: 'DetailDestination', params: { slug: 'jatiluwih' } }"
              class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
            >
              Jatiluwih
              <ArrowUpRight class="size-4" />
            </RouterLink>
            <p class="text-[8px] md:text-[10px] text-neu-50">Photo by jatiluwih.id</p>
          </div>
        </div>
        <div class="w-full lg:w-5/12 flex-col items-center flex">
          <h1
            class="text-2xl md:text-[32px] font-semibold leading-8 md:leading-12 text-center font-se"
          >
            Know a <span class="text-pr-500">Hidden Gem</span> in Bali?
          </h1>
          <p class="mt-3 text-sm md:text-base text-center text-neu-600">
            Share your favorite Bali spot and help fellow travelers discover unique places off the
            beaten path.
          </p>
          <RouterLink
            :to="{ name: 'SuggestSpot' }"
            class="px-6 py-2 mt-6 flex text-sm md:text-base items-center justify-center font-medium leading-6 bg-neu-900 rounded-full text-neu-50"
          >
            Let's Share
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="mt-24 md:mt-30 flex-col flex items-center">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 text-sm sm:text-base items-center justify-center font-medium outline-pr-500 outline rounded-full"
      >
        Benefits
      </div>
      <h1
        class="text-[32px] md:text-[48px] text-center mt-3 font-semibold leading-12 md:leading-[72px] max-w-[590px] font-se"
      >
        <span class="text-pr-500">Why</span> Travel with Us?
      </h1>
      <div class="mt-8 flex flex-col w-full sm:w-auto lg:flex-row gap-8">
        <div class="flex flex-col p-4 lg:p-6 gap-4 lg:gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <Leaf class="text-se-200" />
            </div>
            <h3 class="text-base xl:text-lg leading-5 xl:leading-7 text-neu-900 font-semibold">
              Curated Bali Destinations
            </h3>
            <p class="text-neu-600 text-sm xl:text-base">
              Discover handpicked gems — let Bali amaze you!
            </p>
          </div>
          <div
            class="px-4.5 py-3 text-sm md:text-base flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
        <div class="flex flex-col p-4 lg:p-6 gap-4 lg:gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <AI class="text-se-200" />
            </div>
            <h3 class="text-base xl:text-lg leading-5 xl:leading-7 text-neu-900 font-semibold">
              Smart AI Travel Guide
            </h3>
            <p class="text-neu-600 text-sm xl:text-base">
              Ask anything, anytime — your Bali guide is ready!
            </p>
          </div>
          <div
            class="px-4.5 py-3 text-sm md:text-base flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
        <div class="flex flex-col p-4 lg:p-6 gap-4 lg:gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <Send class="text-se-200" />
            </div>
            <h3 class="text-base xl:text-lg leading-5 xl:leading-7 text-neu-900 font-semibold">
              User-Contributed Spots
            </h3>
            <p class="text-neu-600 text-sm xl:text-base">
              Share your spot, inspire others, shape the Bali journey!
            </p>
          </div>
          <div
            class="px-4.5 py-3 text-sm md:text-base flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
      </div>
    </section>

    <section class="mt-24 md:mt-30">
      <div class="flex flex-col xl:flex-row gap-8 items-center">
        <div class="w-full xl:w-5/12 flex-col items-start flex">
          <div
            class="px-4 text-pr-500 py-2 text-sm sm:text-base flex gap-2 w-fit items-center justify-center font-medium outline-pr-500 outline rounded-full"
          >
            Reviews
          </div>
          <h1
            class="text-[32px] md:text-[48px] mt-3 font-semibold leading-12 md:leading-18 font-se"
          >
            Honest <span class="text-pr-500">Words</span>, Real Stories
          </h1>
          <p
            class="mt-3 text-neu-600 text-sm md:text-base w-full lg:max-w-[560px] xl:max-w-[468px]"
          >
            Explore honest Bali reviews from real travelers and inspire others by sharing your own
            unforgettable island adventures and tips.
          </p>
          <RouterLink
            :to="{ name: 'WriteReview' }"
            class="px-6 py-2 mt-6 flex text-sm md:text-base items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Review & Inspire
          </RouterLink>
        </div>
        <div
          class="relative overflow-hidden w-full xl:w-7/12 h-64 sm:h-72 md:h-80 lg:h-[420px] rounded-3xl"
        >
          <img
            src="@/assets/images/monkey-forest.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div
            class="flex flex-col justify-between absolute bottom-0 right-0 top-0 left-0 p-4 md:p-6"
          >
            <div class="flex justify-between items-start">
              <RouterLink
                :to="{ name: 'DetailDestination', params: { slug: 'monkey-forest' } }"
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Monkey Forest
                <ArrowUpRight class="size-4" />
              </RouterLink>
              <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
            </div>
            <div
              class="flex items-center rounded-2xl md:rounded-3xl bg-sur-50 py-2 md:py-4 px-3 md:px-5"
            >
              <div class="flex gap-4 w-full items-center">
                <div class="flex-col flex gap-1">
                  <DoubleQuotes class="size-6 md:size-8 text-neu-900" />
                  <p class="text-neu-600 text-xs md:text-sm h-8 md:h-10 line-clamp-2">
                    Amazing atmosphere, friendly monkeys, and stunning jungle views — a must-visit
                    cultural and natural gem in Ubud!
                  </p>
                </div>
                <div class="divider w-[1px] h-[50px] bg-neu-100"></div>
                <div class="gap-2 min-w-fit flex items-center">
                  <img
                    src="@/assets/images/User Avatar.jpg"
                    alt="User Profile"
                    class="size-10.5 rounded-full"
                  />
                  <div class="hidden md:flex flex-col gap-[2px]">
                    <p class="flex text-neu-900 font-medium whitespace-nowrap text-xs md:text-sm">
                      Udin Surudin
                    </p>
                    <div class="flex gap-[2px] items-center">
                      <StarFilled class="size-3.5" />
                      <StarFilled class="size-3.5" />
                      <StarFilled class="size-3.5" />
                      <StarFilled class="size-3.5" />
                      <StarFilled class="size-3.5" />
                    </div>
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

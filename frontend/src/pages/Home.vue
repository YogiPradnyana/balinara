<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Search from '@/components/icons/Search.vue'
import heroImage from '@/assets/images/ubud-village.webp'
import Heart from '@/components/icons/Heart.vue'
import Leaf from '@/components/icons/Leaf.vue'
import AI from '@/components/icons/AI.vue'
import Send from '@/components/icons/Send.vue'
import DoubleQuotes from '@/components/icons/DoubleQuotes.vue'
import X from '@/components/icons/social-media/X.vue'
import Instagram from '@/components/icons/social-media/Instagram.vue'
import Youtube from '@/components/icons/social-media/Youtube.vue'
import Threads from '@/components/icons/social-media/Threads.vue'
</script>

<template>
  <div class="container px-[140px]">
    <main class="hero-section flex-col flex items-center gap-8 mt-16">
      <div class="flex flex-col gap-3 text-center items-center">
        <h1 class="text-[48px] font-semibold leading-[62px] font-se">
          Your Journey to <span class="text-pr-500">Bali</span> Starts Here
        </h1>
        <p class="text-neu-600 max-w-[644px]">
          From serene rice fields to lively beach clubs, explore Bali like never before. Ask our AI
          chatbot anything — your digital tour guide is always ready.
        </p>
      </div>
      <form
        class="max-w-[640px] w-full flex items-center justify-between rounded-full outline outline-neu-200 p-1.5"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search />
          <input
            type="text"
            class="w-full text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Search Destionations..."
          />
        </div>
        <button
          type="submit"
          class="px-6 py-2 flex gap-2 items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
        >
          Search
        </button>
      </form>
      <div class="relative overflow-hidden w-full h-[380px] rounded-3xl">
        <img :src="heroImage" alt="Ubud Village" class="object-cover w-full h-full" />
        <div class="flex flex-col justify-between absolute bottom-0 top-0 left-0 p-6">
          <div
            class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
          >
            Ubud Village
            <ArrowUpRight class="size-4" />
          </div>
          <p class="text-[10px] text-neu-50">Photo by unsplash</p>
        </div>
      </div>
    </main>

    <section class="mt-30 flex-col flex gap-3">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center font-medium outline-pr-500 outline rounded-full"
      >
        Destinations
      </div>
      <div class="flex justify-between items-start">
        <h1 class="text-[48px] font-semibold leading-[72px] max-w-[590px] font-se">
          Find The Best <span class="text-pr-500">Destinations</span> in Bali
        </h1>
        <div class="flex gap-4 items-center">
          <p class="text-neu-600 max-w-80 text-end">
            Find your perfect Bali escape — explore beaches, temples, mountains, and local treasures
            effortlessly.
          </p>
          <div class="p-4 flex items-center justify-center bg-pr-500 rounded-full">
            <ArrowUpRight class="size-9 text-neu-50" />
          </div>
        </div>
      </div>
      <div class="mt-8 whitespace-nowrap">
        <div class="flex gap-8 w-fit">
          <div class="overflow-hidden w-[340px] h-[460px] rounded-4xl group">
            <div
              class="relative h-full w-full group-hover:h-86 transition-all duration-500 ease-in-out"
            >
              <img
                src="@/assets/images/ulun-danu-beratan.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-4xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="text-neu-900" />
                </div>
                <div class="flex justify-between items-end w-full">
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                  >
                    Ulun Danu Beratan
                    <ArrowUpRight class="size-4" />
                  </div>
                  <p class="text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
              <div class="w-full px-2">
                <h3 class="text-lg mt-4 leading-7 text-neu-900 font-semibold">Ulun Danu Beratan</h3>
                <p class="text-neu-600 mt-1 line-clamp-2 whitespace-normal">
                  Ulun Danu Beratan is a stunning Balinese Hindu temple located on Lake Beratan,
                  appearing to float.
                </p>
              </div>
            </div>
          </div>
          <div class="overflow-hidden w-[340px] h-[460px] rounded-4xl group">
            <div
              class="relative h-full w-full group-hover:h-86 transition-all duration-500 ease-in-out"
            >
              <img
                src="@/assets/images/ulun-danu-beratan.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-4xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="text-neu-900" />
                </div>
                <div class="flex justify-between items-end w-full">
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                  >
                    Ulun Danu Beratan
                    <ArrowUpRight class="size-4" />
                  </div>
                  <p class="text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
              <div class="w-full px-2">
                <h3 class="text-lg mt-4 leading-7 text-neu-900 font-semibold">Ulun Danu Beratan</h3>
                <p class="text-neu-600 mt-1 line-clamp-2 whitespace-normal">
                  Ulun Danu Beratan is a stunning Balinese Hindu temple located on Lake Beratan,
                  appearing to float.
                </p>
              </div>
            </div>
          </div>
          <div class="overflow-hidden w-[340px] h-[460px] rounded-4xl group">
            <div
              class="relative h-full w-full group-hover:h-86 transition-all duration-500 ease-in-out"
            >
              <img
                src="@/assets/images/ulun-danu-beratan.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-4xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="text-neu-900" />
                </div>
                <div class="flex justify-between items-end w-full">
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                  >
                    Ulun Danu Beratan
                    <ArrowUpRight class="size-4" />
                  </div>
                  <p class="text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
              <div class="w-full px-2">
                <h3 class="text-lg mt-4 leading-7 text-neu-900 font-semibold">Ulun Danu Beratan</h3>
                <p class="text-neu-600 mt-1 line-clamp-2 whitespace-normal">
                  Ulun Danu Beratan is a stunning Balinese Hindu temple located on Lake Beratan,
                  appearing to float.
                </p>
              </div>
            </div>
          </div>
          <div class="overflow-hidden w-[340px] h-[460px] rounded-4xl group">
            <div
              class="relative h-full w-full group-hover:h-86 transition-all duration-500 ease-in-out"
            >
              <img
                src="@/assets/images/ulun-danu-beratan.webp"
                alt="Ubud Village"
                class="object-cover w-full h-full rounded-4xl transition-transform duration-500 ease-in-out"
              />
              <div
                class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
              >
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="text-neu-900" />
                </div>
                <div class="flex justify-between items-end w-full">
                  <div
                    class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                  >
                    Ulun Danu Beratan
                    <ArrowUpRight class="size-4" />
                  </div>
                  <p class="text-[10px] text-neu-50">Photo by unsplash</p>
                </div>
              </div>
              <div class="w-full px-2">
                <h3 class="text-lg mt-4 leading-7 text-neu-900 font-semibold">Ulun Danu Beratan</h3>
                <p class="text-neu-600 mt-1 line-clamp-2 whitespace-normal">
                  Ulun Danu Beratan is a stunning Balinese Hindu temple located on Lake Beratan,
                  appearing to float.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="mt-30">
      <div class="flex gap-8 items-center p-8 rounded-4xl bg-se-50">
        <div class="relative overflow-hidden min-w-[600px] h-[380px] rounded-3xl">
          <img
            src="@/assets/images/jatiluwih.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div class="flex flex-col justify-between absolute bottom-0 top-0 left-0 p-6">
            <div
              class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
            >
              Jatiluwih
              <ArrowUpRight class="size-4" />
            </div>
            <p class="text-[10px] text-neu-50">Photo by jatiluwih.id</p>
          </div>
        </div>
        <div class="w-full flex-col items-center flex">
          <h1 class="text-[32px] font-semibold leading-12 text-center font-se">
            Know a <span class="text-pr-500">Hidden Gem</span> in Bali?
          </h1>
          <p class="mt-3 text-center text-neu-600">
            Share your favorite Bali spot and help fellow travelers discover unique places off the
            beaten path.
          </p>
          <button
            type="button"
            class="px-6 py-2 mt-6 flex gap-2 items-center justify-center font-medium leading-6 bg-neu-900 rounded-full text-neu-50"
          >
            Let's Share
          </button>
        </div>
      </div>
    </section>
    <section class="mt-30 flex-col flex items-center">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center font-medium outline-pr-500 outline rounded-full"
      >
        Benefits
      </div>
      <h1 class="text-[48px] text-center mt-3 font-semibold leading-[72px] max-w-[590px] font-se">
        <span class="text-pr-500">Why</span> Travel with Us?
      </h1>
      <div class="mt-8 flex gap-8">
        <div class="flex flex-col p-6 gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <Leaf class="text-se-200" />
            </div>
            <h3 class="text-lg leading-7 text-neu-900 font-semibold">Curated Bali Destinations</h3>
            <p class="text-neu-600">Discover handpicked gems — let Bali amaze you!</p>
          </div>
          <div
            class="px-4.5 py-3 flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
        <div class="flex flex-col p-6 gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <AI class="text-se-200" />
            </div>
            <h3 class="text-lg leading-7 text-neu-900 font-semibold">Smart AI Travel Guide</h3>
            <p class="text-neu-600">Ask anything, anytime — your Bali guide is ready!</p>
          </div>
          <div
            class="px-4.5 py-3 flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
        <div class="flex flex-col p-6 gap-6 bg-se-50 rounded-3xl">
          <div class="flex flex-col gap-3">
            <div class="p-2.5 flex items-center w-fit justify-center bg-sur-50 rounded-full">
              <Send class="text-se-200" />
            </div>
            <h3 class="text-lg leading-7 text-neu-900 font-semibold">User-Contributed Spots</h3>
            <p class="text-neu-600">Share your spot, inspire others, shape the Bali journey!</p>
          </div>
          <div
            class="px-4.5 py-3 flex gap-1.5 items-center w-fit h-fit justify-center bg-sur-50 rounded-full text-neu-900"
          >
            Learn More
            <ArrowUpRight class="size-5" />
          </div>
        </div>
      </div>
    </section>
    <section class="mt-30">
      <div class="flex gap-8 items-center">
        <div class="w-full flex-col items-start flex">
          <div
            class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center font-medium outline-pr-500 outline rounded-full"
          >
            Reviews
          </div>
          <h1 class="text-[48px] mt-3 font-semibold leading-18 font-se">
            Honest <span class="text-pr-500">Words</span>, Real Stories
          </h1>
          <p class="mt-3 text-neu-600 max-w-[468px]">
            Explore honest Bali reviews from real travelers and inspire others by sharing your own
            unforgettable island adventures and tips.
          </p>
          <button
            type="button"
            class="px-6 py-2 mt-6 flex gap-2 items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Review & Inspire
          </button>
        </div>
        <div class="relative overflow-hidden min-w-[660px] h-[420px] rounded-3xl">
          <img
            src="@/assets/images/monkey-forest.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div class="flex flex-col justify-between absolute bottom-0 right-0 top-0 left-0 p-6">
            <div class="flex justify-between items-start">
              <div
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Monkey Forest
                <ArrowUpRight class="size-4" />
              </div>
              <p class="text-[10px] text-neu-50">Photo by unsplash</p>
            </div>
            <div class="flex items-center rounded-3xl bg-sur-50 py-4 px-5">
              <div class="flex gap-4 items-center">
                <div class="flex-col flex gap-1 max-w-94">
                  <DoubleQuotes class="text-neu-900" />
                  <p class="text-neu-600 text-sm h-10 line-clamp-2">
                    Amazing atmosphere, friendly monkeys, and stunning jungle views — a must-visit
                    cultural and natural gem in Ubud!
                  </p>
                </div>
                <div class="divider w-[1px] h-[50px] bg-neu-100"></div>
                <div class="gap-2 flex items-center">
                  <img
                    src="@/assets/images/User Avatar.jpg"
                    alt="User Profile"
                    class="size-10.5 rounded-full"
                  />
                  <p class="text-neu-900 font-medium text-sm whitespace-nowrap">Udin Surudin</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
  <footer class="mt-30 bg-neu-100 py-20 px-[140px] flex flex-col gap-8">
    <div class="flex justify-between items-start">
      <div class="max-w-[520px]">
        <h1 class="font-se text-[32px] leading-12 font-semibold">
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <p class="text-neu-900 mt-2">
          Your Bali adventure begins here — explore, review, and share unforgettable moments with
          Balinara
        </p>
        <div class="mt-6 flex gap-6 text-neu-900">
          <X />
          <Instagram />
          <Youtube />
          <Threads />
        </div>
      </div>
      <div class="flex gap-16">
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-[18px]">Explore</h3>
          <ul class="flex gap-4 flex-col mt-4.5 text-neu-800">
            <li>Discover</li>
            <li>Write a Review</li>
            <li>Suggest a Spot</li>
            <li>About Us</li>
          </ul>
        </div>
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-[18px]">Support</h3>
          <ul class="flex gap-4 flex-col mt-4.5 text-neu-800">
            <li>Help Center</li>
            <li>FAQs</li>
            <li>Contact Us</li>
          </ul>
        </div>
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-[18px]">Get Inspired</h3>
          <ul class="flex gap-4 flex-col mt-4.5 text-neu-800">
            <li>Bali Travel Tips</li>
            <li>Hidden Gems in Bali</li>
            <li>Top-Rated Spots</li>
            <li>Balinara Blog</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="divider w-full h-[1px] bg-neu-200"></div>
    <div class="flex justify-between text-neu-900">
      <p>© 2025 Balinara. All rights reserved.</p>
      <ul class="flex gap-8 underline">
        <li><a href="#">Privacy Policy</a></li>
        <li><a href="#">Terms of Service</a></li>
        <li><a href="#">Cookies</a></li>
      </ul>
    </div>
  </footer>
</template>

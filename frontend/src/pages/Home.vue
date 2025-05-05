<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Search from '@/components/icons/Search.vue'
import heroImage from '@/assets/images/ubud-village.webp'
import Heart from '@/components/icons/Heart.vue'
</script>

<template>
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
        <div class="relative overflow-hidden w-[340px] h-[460px] rounded-4xl">
          <img
            src="@/assets/images/ulun-danu-beratan.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div
            class="flex flex-col justify-between absolute bottom-0 left-0 top-0 right-0 items-end p-3"
          >
            <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
              <Heart class="text-neu-900" />
            </div>
            <div class="flex justify-between items-end w-full">
              <div
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Ulun Danu Beratan
                <ArrowUpRight class="size-4" />
              </div>
              <p class="text-[10px] text-neu-50">Photo by unsplash</p>
            </div>
          </div>
        </div>
        <div class="relative overflow-hidden w-[340px] h-[460px] rounded-4xl">
          <img
            src="@/assets/images/ulun-danu-beratan.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div
            class="flex flex-col justify-between absolute bottom-0 left-0 top-0 right-0 items-end p-3"
          >
            <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
              <Heart class="text-neu-900" />
            </div>
            <div class="flex justify-between items-end w-full">
              <div
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Ulun Danu Beratan
                <ArrowUpRight class="size-4" />
              </div>
              <p class="text-[10px] text-neu-50">Photo by unsplash</p>
            </div>
          </div>
        </div>
        <div class="relative overflow-hidden w-[340px] h-[460px] rounded-4xl">
          <img
            src="@/assets/images/ulun-danu-beratan.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div
            class="flex flex-col justify-between absolute bottom-0 left-0 top-0 right-0 items-end p-3"
          >
            <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
              <Heart class="text-neu-900" />
            </div>
            <div class="flex justify-between items-end w-full">
              <div
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Ulun Danu Beratan
                <ArrowUpRight class="size-4" />
              </div>
              <p class="text-[10px] text-neu-50">Photo by unsplash</p>
            </div>
          </div>
        </div>
        <div class="relative overflow-hidden w-[340px] h-[460px] rounded-4xl">
          <img
            src="@/assets/images/ulun-danu-beratan.webp"
            alt="Ubud Village"
            class="object-cover w-full h-full"
          />
          <div
            class="flex flex-col justify-between absolute bottom-0 left-0 top-0 right-0 items-end p-3"
          >
            <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
              <Heart class="text-neu-900" />
            </div>
            <div class="flex justify-between items-end w-full">
              <div
                class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-sm bg-sur-50 rounded-full text-neu-900"
              >
                Ulun Danu Beratan
                <ArrowUpRight class="size-4" />
              </div>
              <p class="text-[10px] text-neu-50">Photo by unsplash</p>
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
</template>

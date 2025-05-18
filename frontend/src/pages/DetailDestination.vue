<script setup>
import ArrowLeft from '@/components/icons/ArrowLeft.vue'
import ArrowRight2 from '@/components/icons/ArrowRight2.vue'
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Call from '@/components/icons/Call.vue'
import DoubleQuotes from '@/components/icons/DoubleQuotes.vue'
import FreeWifi from '@/components/icons/facilities/FreeWifi.vue'
import Guide from '@/components/icons/facilities/Guide.vue'
import Parking from '@/components/icons/facilities/Parking.vue'
import Restaurant from '@/components/icons/facilities/Restaurant.vue'
import SouvenirShop from '@/components/icons/facilities/SouvenirShop.vue'
import Toilet from '@/components/icons/facilities/Toilet.vue'
import Heart from '@/components/icons/Heart.vue'
import Location from '@/components/icons/Location.vue'
import Mail from '@/components/icons/Mail.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Temple from '@/components/icons/Temple.vue'
</script>
<template>
  <!-- Main Content -->
  <div class="px-6 sm:px-16 lg:px-[140px]">
    <!-- Breadcrumb -->
    <nav class="flex gap-1 mt-10 md:mt-14 items-center">
      <ArrowLeft />
      <div class="flex gap-2 text-sm sm:text-base items-center text-neu-500">
        <a href="#" class="text-neu-900"><span>Discover</span></a>
        /
        <span>Tanah Lot</span>
      </div>
    </nav>

    <!-- Hero Section -->
    <div
      class="grid grid-rows-3 lg:grid-rows-1 lg:grid-cols-3 gap-2 sm:gap-3 mt-4 md:mt-8 h-96 sm:h-[435px]"
    >
      <div class="relative w-full h-full row-span-2 lg:row-span-1 lg:col-span-2">
        <img
          src="@/assets/images/tanah-lot-1.webp"
          alt="Tanah Lot"
          class="absolute inset-0 w-full h-full object-cover rounded-[20px]"
        />
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-1 lg:grid-rows-2 gap-2 sm:gap-3 h-full">
        <div class="relative w-full h-full">
          <img
            src="@/assets/images/tanah-lot-2.webp"
            alt="Tanah Lot 2"
            class="absolute inset-0 w-full h-full object-cover rounded-[20px]"
          />
        </div>
        <div class="relative w-full h-full">
          <img
            src="@/assets/images/tanah-lot-3.webp"
            alt="Tanah Lot 3"
            class="absolute inset-0 w-full h-full object-cover rounded-[20px]"
          />
        </div>
      </div>
    </div>

    <!-- Info Section -->
    <section class="mb-8 mt-13">
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-8 sm:gap-16">
        <div class="xl:col-span-2">
          <div>
            <div class="flex items-start gap-2 sm:items-center justify-between">
              <h1 class="text-3xl md:text-4xl lg:text-[42px] font-se font-semibold leading-12">
                Tanah Lot
              </h1>
              <div class="flex gap-1.5 sm:gap-2.5">
                <div
                  class="bg-[#F1F8F9] text-sm sm:text-base px-4 gap-2 py-2 rounded-full font-medium items-center text-se-500 flex"
                >
                  <Temple class="size-5 sm:size-6 hidden sm:block" />
                  Temple
                </div>
                <div
                  class="px-2 sm:px-4 border-neu-200 text-sm sm:text-base border-[1.6px] gap-2 py-2 rounded-full font-medium items-center flex"
                >
                  <Heart class="size-5 sm:size-6" />
                  <span class="hidden sm:block">Save</span>
                </div>
              </div>
            </div>

            <div class="gap-1 font-medium text-sm sm:text-base items-center mt-1 flex">
              <Location class="size-5 sm:size-6" />Beraban Village, Kediri, Tabanan
            </div>

            <p class="mt-4 sm:mt-6 text-neu-500 text-sm sm:text-base">
              Tanah Lot Temple is an iconic Balinese sea temple perched dramatically on a rock
              formation just off the coast. This ancient Hindu shrine is dedicated to the sea gods
              and is renowned for its stunning ocean views, especially during sunset. The temple’s
              name literally translates to “Land in the Sea,” perfectly describing its unique
              offshore setting. Often regarded as one of Bali’s most important landmarks, Tanah Lot
              not only offers breathtaking scenery but also holds deep spiritual significance for
              the local Balinese people.
            </p>
          </div>
          <!-- Facilities -->
          <div class="mt-6 sm:mt-8">
            <h2 class="text-lg sm:text-xl font-semibold mb-4">Facilities</h2>
            <ul class="flex flex-wrap text-sm sm:text-base gap-3 sm:gap-4">
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <Parking class="size-5 sm:size-6" />Parking Area
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <Toilet class="size-5 sm:size-6" />Restrooms
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <Guide class="size-5 sm:size-6" />Guided Tours
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <Restaurant class="size-5 sm:size-6" />Restaurant
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <FreeWifi class="size-5 sm:size-6" />Free Wi-Fi
              </li>
              <li
                class="bg-[#F2F8F5] text-pr-500 gap-2 font-medium items-center px-4 py-2 rounded-full flex"
              >
                <SouvenirShop class="size-5 sm:size-6" />Souvenir Shop
              </li>
            </ul>
          </div>
        </div>

        <div
          class="p-6 border-neu-200 text-sm sm:text-base max-w-120 xl:w-full h-fit border rounded-3xl"
        >
          <div class="gap-3 flex flex-col">
            <p class="font-medium text-base">Entrance Ticket</p>
            <p class="ml-6">Rp 75.000 - 120.000</p>
          </div>
          <div class="gap-3 flex flex-col mt-6">
            <p class="font-medium text-base">Contact Person</p>
            <div class="ml-6 flex flex-col gap-3">
              <p class="flex items-center gap-2">
                <Call class="size-5 sm:size-6" />+62 812-3456-7890
              </p>
              <p class="flex items-center gap-2">
                <Mail class="size-5 sm:size-6" />hello@balinara.id
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Location Map -->
    <section class="mt-8sm:mt-16">
      <h2 class="text-xl font-semibold mb-4">Location</h2>
      <div class="w-full h-64 sm:h-[420px] rounded-3xl overflow-hidden">
        <iframe
          class="w-full h-full"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126716.86249239304!2d115.00318589688208!3d-8.620116957947658!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd2465b5ed1c7c3%3A0x60ee9fa80ff10d53!2sTanah%20Lot!5e0!3m2!1sen!2sid!4v1715437775084!5m2!1sen!2sid"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        >
        </iframe>
      </div>
    </section>

    <!-- Reviews -->
    <section class="mt-24 sm:mt-30">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Reviews
      </div>

      <div class="flex flex-col mt-3 lg:flex-row lg:justify-between items-start">
        <h2
          class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] max-w-[590px] font-se"
        >
          Traveler <span class="text-pr-500">Insights</span> You Can Trust
        </h2>
        <div class="flex gap-2 md:gap-4 mt-3 items-center">
          <p class="text-neu-600 text-sm sm:text-base max-w-full lg:max-w-80 lg:text-end">
            Add your own experience to guide and inspire more travelers exploring this amazing
            destination.
          </p>
          <div class="p-4 flex items-center justify-center bg-pr-500 rounded-full">
            <ArrowUpRight class="size-5 sm:size-9 text-neu-50" />
          </div>
        </div>
      </div>

      <!-- Review cards -->
      <div class="flex flex-col md:flex-row gap-8 mt-8">
        <div
          v-for="i in 2"
          :key="i"
          class="flex items-center rounded-2xl md:rounded-3xl outline-neu-200 outline-1 bg-sur-50 py-2 md:py-4 px-3 md:px-5"
        >
          <div class="w-full">
            <div class="flex-col flex gap-2">
              <DoubleQuotes class="size-6 sm:size-8 text-neu-900" />
              <p class="text-neu-600 text-sm sm:text-base h-10 sm:h-12 line-clamp-2">
                The sunset at Tanah Lot was absolutely breathtaking! A magical moment I’ll remember
                forever.
              </p>
            </div>
            <div class="flex mt-1.5 gap-1 items-center">
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
              <StarFilled class="size-5 sm:size-6" />
            </div>
            <div class="gap-2 mt-3 min-w-fit flex items-center">
              <img
                src="@/assets/images/User Avatar.jpg"
                alt="User Profile"
                class="size-9 sm:size-10.5 rounded-full"
              />
              <p class="text-neu-900 font-medium whitespace-nowrap text-xs sm:text-sm">
                Udin Surudin
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Explores -->
    <section class="mt-24 sm:mt-30">
      <div
        class="px-4 text-pr-500 py-2 flex gap-2 w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Explore
      </div>

      <div class="flex flex-col mt-3">
        <h2 class="text-[32px] md:text-[48px] font-semibold leading-12 md:leading-[72px] font-se">
          Your Next Bali <span class="text-pr-500">Adventure</span> Awaits
        </h2>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <p class="text-neu-600 text-sm max-w-[746px] sm:text-base mt-3">
            Let the magic of Bali lead you to new places. Keep scrolling, keep exploring — your next
            adventure is just a click away.
          </p>
          <div
            class="cursor-pointer w-fit whitespace-nowrap flex px-5.5 py-2 gap-1 items-center justify-center text-sm sm:text-base font-medium bg-pr-500 rounded-full text-white"
          >
            View All
            <ArrowRight2 class="min-w-6" />
          </div>
        </div>
      </div>

      <div class="flex gap-6 mt-8 w-fit">
        <div v-for="i in 4" :key="i" class="overflow-hidden w-80 sm:w-[340px] h-fit group">
          <div class="relative h-fit w-full">
            <img
              src="@/assets/images/mount-agung.webp"
              alt="Ubud Village"
              class="object-cover w-full h-52 sm:h-60 rounded-3xl transition-transform duration-500 ease-in-out"
            />
            <div
              class="flex flex-col justify-between absolute inset-0 items-end p-3 transition-opacity duration-500 ease-in-out"
            >
              <div class="flex items-center justify-between w-full">
                <div
                  class="py-1 px-2.5 flex items-center justify-center font-medium text-sm gap-1 bg-sur-50 rounded-full"
                >
                  <StarFilled class="size-4 md:size-4.5" />
                  4.8
                </div>
                <div class="p-2.5 flex items-center justify-center bg-sur-50 rounded-full">
                  <Heart class="size-5 md:size-6 text-neu-900" />
                </div>
              </div>
              <div class="flex justify-between items-end w-full">
                <div
                  class="px-4 py-2.5 flex gap-1.5 items-center w-fit h-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900 transition-all duration-500 ease-in-out"
                >
                  Mount Agung
                  <ArrowUpRight class="size-4" />
                </div>
                <p class="text-[8px] md:text-[10px] text-neu-50">Photo by unsplash</p>
              </div>
            </div>
          </div>
          <div class="w-full px-2 mt-2 sm:mt-4">
            <h3 class="text-base sm:text-lg leading-7 text-neu-900 font-semibold">Mount Agung</h3>
            <p class="text-sm sm:text-base text-neu-600 mt-1 line-clamp-2 whitespace-normal">
              Mount Agung is Bali's highest and most sacred mountain, presenting a challenging trek
              with stunning vistas and significant spiritual importance to the Balinese people.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

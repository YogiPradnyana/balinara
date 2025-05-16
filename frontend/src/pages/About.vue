<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import Bali from '@/components/icons/Bali.vue'
import Call from '@/components/icons/Call.vue'
import Mail from '@/components/icons/Mail.vue'
import OutlinedLocation from '@/components/icons/OutlinedLocation.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px]">
    <!-- Hero Section -->
    <section class="h-[560px] mt-16 overflow-hidden rounded-3xl">
      <div class="relative h-full w-full">
        <img src="@/assets/images/diamond-beach.webp" alt="" class="object-cover w-full h-full" />

        <div class="absolute inset-0 flex flex-col p-6 justify-between">
          <div class="flex justify-end">
            <div
              class="px-4 py-2.5 flex gap-1.5 items-center w-fit justify-center text-xs md:text-sm bg-sur-50 rounded-full text-neu-900"
            >
              Diamond Beach
              <ArrowUpRight class="size-4" />
            </div>
          </div>
          <div class="bg-sur-50 p-6 w-full md:max-w-[575px] rounded-2xl shadow-lg">
            <div
              class="px-4 text-pr-500 py-2 flex w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
            >
              About Balinara
            </div>
            <h1
              class="text-4xl my-2 sm:my-3 sm:text-[48px] font-semibold leading-12 sm:leading-[62px] font-se"
            >
              Your Curated <span class="text-pr-500">Gateway</span> to the Heart of Bali.
            </h1>
            <p class="text-neu-600 text-sm mb-4 sm:mb-6 sm:text-base">
              Discover handpicked experiences, iconic landmarks, and hidden gems—each destination
              chosen to immerse you in the soul of Bali’s culture and beauty.
            </p>

            <RouterLink
              :to="{ name: 'Destinations' }"
              class="px-6 py-2 flex items-center w-fit justify-center text-sm sm:text-base font-medium bg-pr-500 rounded-full text-neu-50"
            >
              Let's Explore
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Story Section -->
    <section class="mt-24 sm:mt-30">
      <div
        class="px-4 mx-auto text-pr-500 py-2 flex w-fit items-center justify-center text-sm sm:text-base font-medium outline-pr-500 outline rounded-full"
      >
        Story
      </div>

      <h1
        class="text-4xl mt-3 text-center sm:text-[42px] font-semibold leading-12 sm:leading-[62px] font-se"
      >
        It All <span class="text-pr-500">Started</span> with Bali…
      </h1>
      <p class="max-w-md md:max-w-xl mt-12 text-sm sm:text-base text-neu-600">
        Balinara started with a simple realization: despite Bali’s global fame, finding truly
        authentic travel experiences wasn’t always easy. Many destinations felt overexposed, while
        hidden gems remained, well… hidden. As passionate travelers and locals, we saw an
        opportunity — to bridge that gap and help people see Bali in a deeper, more meaningful way.
      </p>

      <Bali class="mx-auto mt-6 sm:mt-4 max-w-[520px]" />
      <p
        class="max-w-md md:max-w-xl mt-6 sm:mt-4 text-sm sm:text-base text-neu-600 text-end ml-auto"
      >
        We curated Balinara not just as a website, but as a travel companion — smart, local, and
        human. With community-driven spots, honest reviews, and an AI travel guide by your side,
        Balinara helps you explore Bali like a friend who truly knows the island. This is our story,
        and now we invite you to be part of it.
      </p>
    </section>

    <!-- Contact Section -->
    <section class="mt-24 sm:mt-30">
      <div class="flex flex-col md:flex-row gap-10 md:gap-8">
        <!-- Info -->
        <div class="flex flex-col">
          <h1 class="text-4xl sm:text-[42px] font-semibold leading-12 sm:leading-[62px] font-se">
            Information <span class="text-pr-500">Contact</span>
          </h1>
          <p class="text-neu-600 text-sm sm:text-base mb-6">
            We are available to answer your inquiries or suggestions. Get in touch with us, and our
            team will respond as soon as possible.
          </p>
          <ul class="flex flex-col gap-6">
            <li class="flex items-center gap-2 text-sm sm:text-base font-medium">
              <Call class="size-5 sm:size-6" />+62 812-3456-7890
            </li>
            <li class="flex items-center gap-2 text-sm sm:text-base font-medium">
              <Mail class="size-5 sm:size-6" />hello@balinara.id
            </li>
            <li class="flex items-center gap-2 text-sm sm:text-base font-medium">
              <OutlinedLocation class="size-5 sm:size-6" />Jl. Raya Nara No.123, Denpasar, Bali
              80232, Indonesia
            </li>
          </ul>
        </div>

        <!-- Contact Form -->
        <div
          class="p-4 sm:p-6 rounded-3xl min-w-full md:min-w-100 xl:min-w-[480px] border border-neu-200"
        >
          <h4 class="font-semibold text-2xl sm:text-[32px]">Contact Us</h4>
          <p class="text-neu-600 text-sm sm:text-base mb-6">
            Feel free to contact us at your convenience.
          </p>
          <form class="flex flex-col gap-4">
            <div class="flex gap-4">
              <input
                type="text"
                placeholder="Firstname"
                class="px-3 w-1/2 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
              <input
                type="text"
                placeholder="Lastname"
                class="px-3 w-1/2 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
              />
            </div>
            <input
              type="email"
              placeholder="Email"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
            <input
              type="text"
              placeholder="Phone"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
            <textarea
              rows="7"
              placeholder="Message"
              class="px-3 py-3 text-sm placeholder:text-neu-500 border border-neu-200 rounded-3xl"
            ></textarea>
            <button type="submit" class="bg-pr-500 text-neu-50 px-6 py-3 font-medium rounded-full">
              Send
            </button>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

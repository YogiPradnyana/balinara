<script setup>
import X from '@/components/icons/social-media/X.vue'
import Instagram from '@/components/icons/social-media/Instagram.vue'
import Youtube from '@/components/icons/social-media/Youtube.vue'
import Threads from '@/components/icons/social-media/Threads.vue'
</script>
<template>
  <footer class="font-pr bg-neu-100 py-16 md:py-20 px-6 sm:px-16 lg:px-[140px] flex flex-col gap-8">
    <div class="flex justify-between flex-wrap items-start">
      <div class="max-w-full xl:max-w-[520px] mb-12">
        <h1 class="font-se text-2xl md:text-[32px] leading-8 md:leading-12 font-semibold">
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <p class="text-neu-900 text-sm md:text-base mt-2">
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
      <div class="flex flex-wrap text-sm md:text-base gap-10 md:gap-16">
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-base md:text-[18px]">Explore</h3>
          <ul class="flex gap-4 flex-col mt-4.5 text-neu-800">
            <li>Discover</li>
            <li>Write a Review</li>
            <li>Suggest a Spot</li>
            <li>About Us</li>
          </ul>
        </div>
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-base md:text-[18px]">Support</h3>
          <ul class="flex gap-4 flex-col mt-4.5 text-neu-800">
            <li>Help Center</li>
            <li>FAQs</li>
            <li>Contact Us</li>
          </ul>
        </div>
        <div class="wrapper">
          <h3 class="text-neu-900 font-medium text-base md:text-[18px]">Get Inspired</h3>
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
    <div class="flex justify-between gap-4 flex-wrap text-sm md:text-base text-neu-900">
      <p>© 2025 Balinara. All rights reserved.</p>
      <ul class="flex gap-6 md:gap-8 underline">
        <li><a href="#">Privacy Policy</a></li>
        <li><a href="#">Terms of Service</a></li>
        <li><a href="#">Cookies</a></li>
      </ul>
    </div>
  </footer>
</template>

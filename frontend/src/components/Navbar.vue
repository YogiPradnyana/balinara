<script setup>
import Login from './icons/Login.vue'
import Search from './icons/Search.vue'
</script>

<template>
  <nav class="px-[100px] font-pr">
    <div class="px-10 py-4 flex justify-between items-center border-b-[1.6px] border-neu-100">
      <h1 class="font-se text-[32px] leading-[38px] font-semibold">
        Bali<span class="text-pr-500">nara</span>
      </h1>
      <form
        class="hidden max-w-[560px] w-full flex items-center justify-between rounded-full outline outline-neu-200 p-1"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search />
          <input
            type="text"
            class="w-full text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Type something here..."
          />
        </div>
        <button
          type="submit"
          class="px-6 py-1.5 flex gap-2 items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
        >
          Search
        </button>
      </form>
      <ul class="flex gap-[60px] items-center">
        <li>Discover</li>
        <li>Review</li>
        <li>About</li>
      </ul>
      <div
        class="px-4.5 py-2.5 flex gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
      >
        <Login />
        Sign in
      </div>
    </div>
  </nav>
</template>

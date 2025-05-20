<script setup>
import ArrowUpRight from '@/components/icons/ArrowUpRight.vue'
import HeartFilled from '@/components/icons/HeartFilled.vue'
import Location from '@/components/icons/Location.vue'
import StarFilled from '@/components/icons/StarFilled.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>
<template>
  <div class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30">
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4 w-full">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Profile</h1>
        <div class="flex flex-col md:flex-row gap-8 w-full">
          <div class="flex flex-col items-center">
            <img src="https://i.pravatar.cc/200" class="size-32 md:size-40 rounded-full" />
            <button
              type="button"
              class="cursor-pointer bg-sur-50 hover:bg-[#e9e9e965] text-sm sm:text-base mt-4 py-2 px-4.5 border border-neu-200 font-medium rounded-full"
            >
              Change Photo
            </button>
            <p
              class="w-3/4 md:max-w-60 lg:max-w-52 xl:max-w-80 text-center text-neu-500 text-sm mt-3"
            >
              Photo format must be .jpg, .jpeg, or .png with a maximum file size of 2MB.
            </p>
          </div>
          <div class="flex flex-col flex-1">
            <h3 class="font-semibold mb-4 text-base sm:text-lg">Pengaturan Profil</h3>
            <form class="space-y-4">
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">Username</label>
                <input
                  type="text"
                  value="Udin Surudin"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">Email</label>
                <input
                  type="email"
                  value="udinganteng@gmail.com"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">Phone Number</label>
                <input
                  type="text"
                  value="081234567891"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>

              <div class="flex justify-end">
                <button
                  class="bg-pr-200 text-sm sm:text-base font-medium text-neu-50 py-2 px-6 rounded-full"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
        <div class="flex mt-8 flex-col md:flex-row gap-5 md:gap-8 w-full">
          <div class="flex flex-col">
            <h3 class="font-semibold text-base sm:text-lg mb-1">Change Password</h3>
            <p class="w-full md:max-w-60 lg:max-w-52 xl:max-w-80 text-neu-500 text-sm">
              Make sure your account uses a long and random password to stay secure.
            </p>
          </div>
          <div class="flex flex-col flex-1">
            <form class="space-y-4">
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">Current Password</label>
                <input
                  type="password"
                  autocomplete="true"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">New Password</label>
                <input
                  type="password"
                  autocomplete="true"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label class="text-sm font-semibold">Confirmation Password</label>
                <input
                  type="password"
                  autocomplete="true"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>

              <div class="flex justify-end">
                <button
                  class="bg-pr-200 text-sm sm:text-base font-medium text-neu-50 py-2 px-6 rounded-full"
                >
                  Change Password
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

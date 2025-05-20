<script setup lang="ts">
import Footer from '@/components/Footer.vue'
import ArrowLeft from '@/components/icons/ArrowLeft.vue'
</script>

<template>
  <div class="px-4 py-10 max-w-6xl mx-auto">
    <div class="min-h-screen bg-white flex">
      <!-- Sidebar -->
      <aside class="w-72 border-r border-neu-200 px-6 py-6 hidden md:block">
        <div class="flex mb-[24px] items-center gap-2">
          <img
            src="@/assets/images/User Avatar.jpg"
            class="w-20 h-20 rounded-full mb-3"
            alt="Profile"
          />
          <div class="">
            <p class="text-[14px] font-semibold">Udin Surudin</p>
            <p class="text-[12px] text-gray-500">udinganteng@gmail.com</p>
          </div>
        </div>

        <nav class="pace-y-3">
          <div
            href="#"
            class="flex items-center text-sm font-medium hover:bg-neu-100 text-neu-900 hover:text-pr-500 py-2 px-2 rounded-xl"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="size-5 mr-2"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M9.90621 10.5157H9.93288C12.3729 10.5157 14.357 8.5315 14.357 6.0915C14.357 3.6515 12.3729 1.6665 9.93288 1.6665C7.49204 1.6665 5.50705 3.6515 5.50705 6.089C5.49871 8.52234 7.47121 10.5082 9.90621 10.5157ZM6.69705 6.0915C6.69705 4.30734 8.14871 2.8565 9.93288 2.8565C11.7162 2.8565 13.167 4.30734 13.167 6.0915C13.167 7.87484 11.7162 9.3265 9.93288 9.3265H9.90871C8.13205 9.31984 6.69121 7.86984 6.69705 6.0915Z"
                fill="#909090"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M3.33203 15.1443C3.33203 18.2251 8.30036 18.2251 9.93286 18.2251C12.7654 18.2251 16.532 17.9076 16.532 15.161C16.532 12.0801 11.5654 12.0801 9.93286 12.0801C7.09953 12.0801 3.33203 12.3976 3.33203 15.1443ZM4.58203 15.1443C4.58203 13.9401 6.38203 13.3301 9.93286 13.3301C13.4829 13.3301 15.282 13.946 15.282 15.161C15.282 16.3651 13.4829 16.9751 9.93286 16.9751C6.38203 16.9751 4.58203 16.3593 4.58203 15.1443Z"
                fill="#909090"
              />
            </svg>
            Profile
          </div>

          <div
            href="#"
            class="flex items-center text-sm font-medium hover:bg-neu-100 text-neu-900 hover:text-pr-500 py-2 px-2 rounded-xl"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="size-5 mr-2"
            >
              <mask
                id="mask0_282_1556"
                style="mask-type: luminance"
                maskUnits="userSpaceOnUse"
                x="1"
                y="2"
                width="18"
                height="17"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M1.66797 2.5H18.7284V18.7508H1.66797V2.5Z"
                  fill="white"
                />
              </mask>
              <g mask="url(#mask0_282_1556)">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M3.1875 10.1026C4.35584 13.7376 8.97167 16.6768 10.1983 17.4043C11.4292 16.6693 16.0783 13.6976 17.2092 10.106C17.9517 7.78431 17.2625 4.84348 14.5242 3.96098C13.1975 3.53514 11.65 3.79431 10.5817 4.62098C10.3583 4.79264 10.0483 4.79598 9.82334 4.62598C8.69167 3.77514 7.21334 3.52598 5.86584 3.96098C3.13167 4.84264 2.445 7.78348 3.1875 10.1026ZM10.1996 18.7509C10.0963 18.7509 9.99377 18.7259 9.90043 18.6751C9.6396 18.5326 3.49543 15.1459 1.99793 10.4843C1.9971 10.4843 1.9971 10.4834 1.9971 10.4834C1.0571 7.54843 2.10377 3.8601 5.48293 2.77093C7.0696 2.2576 8.79877 2.48343 10.1971 3.36593C11.5521 2.50927 13.3521 2.2726 14.9071 2.77093C18.2896 3.86177 19.3396 7.54926 18.4004 10.4834C16.9513 15.0918 10.7621 18.5293 10.4996 18.6734C10.4063 18.7251 10.3029 18.7509 10.1996 18.7509Z"
                  fill="#909090"
                />
              </g>
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M15.1302 8.85406C14.8077 8.85406 14.5344 8.60656 14.5077 8.27989C14.4527 7.59489 13.9944 7.01656 13.3419 6.80573C13.0127 6.69906 12.8327 6.34656 12.9385 6.01906C13.046 5.69073 13.3952 5.51239 13.7252 5.61573C14.861 5.98323 15.6569 6.98906 15.7544 8.17823C15.7819 8.52239 15.526 8.82406 15.1819 8.85156C15.1644 8.85323 15.1477 8.85406 15.1302 8.85406Z"
                fill="#909090"
              />
            </svg>
            Wishlist
          </div>

          <div
            href="#"
            class="flex items-center text-sm font-medium hover:bg-neu-100 text-neu-900 hover:text-pr-500 py-2 px-2 rounded-xl"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="size-5 mr-2"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M9.7928 3.75C9.71697 3.75 9.5303 3.77083 9.43113 3.96917L7.90947 7.01167C7.66863 7.4925 7.20447 7.82667 6.6678 7.90333L3.26113 8.39417C3.03613 8.42667 2.95947 8.59333 2.93613 8.66333C2.9153 8.73083 2.88197 8.9025 3.03697 9.05083L5.5003 11.4175C5.8928 11.795 6.07113 12.3392 5.9778 12.8717L5.3978 16.2133C5.36197 16.4225 5.4928 16.5442 5.55113 16.5858C5.6128 16.6325 5.7778 16.725 5.98197 16.6183L9.0278 15.0392C9.5078 14.7917 10.0795 14.7917 10.5578 15.0392L13.6028 16.6175C13.8078 16.7233 13.9728 16.6308 14.0353 16.5858C14.0936 16.5442 14.2245 16.4225 14.1886 16.2133L13.607 12.8717C13.5136 12.3392 13.692 11.795 14.0845 11.4175L16.5478 9.05083C16.7036 8.9025 16.6703 8.73 16.6486 8.66333C16.6261 8.59333 16.5495 8.42667 16.3245 8.39417L12.9178 7.90333C12.382 7.82667 11.9178 7.4925 11.677 7.01083L10.1536 3.96917C10.0553 3.77083 9.86863 3.75 9.7928 3.75ZM5.7904 17.9167C5.44623 17.9167 5.10457 17.8083 4.81207 17.595C4.30707 17.225 4.05957 16.6142 4.16707 15.9992L4.74707 12.6575C4.76873 12.5333 4.72623 12.4075 4.63457 12.3192L2.17123 9.9525C1.7179 9.51833 1.5554 8.87667 1.74707 8.28083C1.9404 7.67833 2.45207 7.2475 3.0829 7.1575L6.48957 6.66667C6.62123 6.64833 6.73457 6.5675 6.79123 6.4525L8.31373 3.40917C8.59457 2.84833 9.16123 2.5 9.7929 2.5C10.4246 2.5 10.9912 2.84833 11.2721 3.40917L12.7954 6.45167C12.8529 6.5675 12.9654 6.64833 13.0962 6.66667L16.5029 7.1575C17.1337 7.2475 17.6454 7.67833 17.8387 8.28083C18.0304 8.87667 17.8671 9.51833 17.4137 9.9525L14.9504 12.3192C14.8587 12.4075 14.8171 12.5333 14.8387 12.6567L15.4196 15.9992C15.5262 16.615 15.2787 17.2258 14.7729 17.595C14.2604 17.9708 13.5929 18.0217 13.0271 17.7267L9.9829 16.1492C9.86373 16.0875 9.72123 16.0875 9.60207 16.1492L6.5579 17.7275C6.31457 17.8542 6.05207 17.9167 5.7904 17.9167Z"
                fill="#909090"
              />
            </svg>
            Review
          </div>

          <div
            href="#"
            class="flex items-center text-sm text-pr-500 font-medium bg-neu-100 py-2 px-2 rounded-xl"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="size-5 mr-2"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M10.2083 7.08333C9.40417 7.08333 8.75 7.7375 8.75 8.5425C8.75 9.34667 9.40417 10 10.2083 10C11.0125 10 11.6667 9.34667 11.6667 8.5425C11.6667 7.7375 11.0125 7.08333 10.2083 7.08333M10.2083 11.2502C8.715 11.2502 7.5 10.036 7.5 8.54266C7.5 7.0485 8.715 5.8335 10.2083 5.8335C11.7017 5.8335 12.9167 7.0485 12.9167 8.54266C12.9167 10.036 11.7017 11.2502 10.2083 11.2502"
                fill="#40916C"
              />
              <mask
                id="mask0_282_1562"
                style="mask-type: luminance"
                maskUnits="userSpaceOnUse"
                x="3"
                y="1"
                width="15"
                height="17"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M3.33398 1.6665H17.0836V17.9165H3.33398V1.6665Z"
                  fill="white"
                />
              </mask>
              <g mask="url(#mask0_282_1562)">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M10.207 2.9165C7.10536 2.9165 4.58203 5.464 4.58203 8.594C4.58203 12.5765 9.2687 16.4565 10.207 16.6632C11.1454 16.4557 15.832 12.5757 15.832 8.594C15.832 5.464 13.3087 2.9165 10.207 2.9165V2.9165ZM10.207 17.9165C8.71203 17.9165 3.33203 13.2898 3.33203 8.594C3.33203 4.774 6.4162 1.6665 10.207 1.6665C13.9979 1.6665 17.082 4.774 17.082 8.594C17.082 13.2898 11.702 17.9165 10.207 17.9165V17.9165Z"
                  fill="#40916C"
                />
              </g>
            </svg>
            Suggest
          </div>
        </nav>
      </aside>

      <!-- Main Content -->
      <div class="flex-1 max-w-3xl mx-auto py-10 px-4">
        <!-- Breadcrumb -->
        <nav class="text-[16px] font-medium mb-[24px] flex">
          <ArrowLeft class="text-neu-900 hover:underline cursor-pointer mr-2" />
          <p>Suggest / <span class="text-neu-500"> Detail</span></p>
        </nav>

        <h1 class="text-[32px] font-semibold mb-[24px]">Detail</h1>

        <!-- Form -->
        <form class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 mb-[24px] gap-6">
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]">Name</label>
              <input
                type="text"
                placeholder="e.g., Hidden Gem Beach Club"
                class="w-full border border-neu-200 rounded-full px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]">Category</label>
              <select class="w-full text-neu-500 border-neu-200 border rounded-full px-3 py-2">
                <option>Select a category — Beach, Temple, Mountain, etc.</option>
              </select>
            </div>
          </div>

          <div class="">
            <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
              >Descriptions</label
            >
            <textarea
              class="w-full border-neu-200 border rounded-2xl px-3 py-2 h-24"
              placeholder="Tell us what makes this place special..."
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
                >Entrance Ticket</label
              >
              <div class="flex gap-2">
                <input
                  type="text"
                  placeholder="Rp 75.000"
                  class="w-screen border-neu-200 border rounded-full px-3 py-2"
                />
                <span class="self-center">-</span>
                <input
                  type="text"
                  placeholder="Rp 120.000"
                  class="w-screen border-neu-200 border rounded-full px-3 py-2"
                />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]">Facilities</label>
            <div class="flex gap-2 flex-wrap mb-[12px]">
              <span class="bg-neu-100 text-pr-500 px-3 py-1 rounded-full text-sm"
                >Parking Area ✕</span
              >
              <span class="bg-neu-100 text-pr-500 px-3 py-1 rounded-full text-sm">Restrooms ✕</span>
            </div>
            <select class="w-full border text-neu-500 border-neu-200 rounded-3xl px-3 py-2">
              <option>Select a facility option</option>
            </select>
          </div>

          <!-- Contact and Map -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
                >Phone Number</label
              >
              <input
                type="text"
                placeholder="e.g., +62 812 3456 7890"
                class="w-full border-neu-200 border rounded-3xl px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]">Mail</label>
              <input
                type="email"
                placeholder="e.g., info@spot.com"
                class="w-full border-neu-200 border rounded-3xl px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]">Street</label>
              <input
                type="text"
                placeholder="e.g., Jalan Pantai Kuta"
                class="w-full border-neu-200 border rounded-3xl px-3 py-2 mb-[12px]"
              />

              <div>
                <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
                  >Sub-district</label
                >
                <input
                  type="text"
                  placeholder="e.g., Kuta"
                  class="w-full border-neu-200 border rounded-3xl px-3 py-2 mb-[12px]"
                />
              </div>

              <div>
                <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
                  >Regency</label
                >
                <input
                  type="text"
                  placeholder="e.g., Badung"
                  class="w-full border-neu-200 border rounded-3xl px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label class="block text-neu-900 text-[18px] font-semibold mb-[12px]"
                >Map Location</label
              >
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126529.1079934922!2d115.0920039!3d-8.3405389!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd216420484e4ef%3A0x5030bfbca7c84f0!2sBali!5e0!3m2!1sid!2sid!4v1715934323456!5m2!1sid!2sid"
                width="100%"
                height="230"
                style="border: 0"
                allowfullscreen="true"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                class="rounded-3xl shadow"
              ></iframe>
            </div>
          </div>

          <!-- Coordinates -->
          <h1 class="text-neu-900 text-[18px] font-semibold mb-[12px]">Coordinate</h1>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-neu-900 text-[16px] font-medium mb-[12px]">Latitude</label>
              <input
                type="text"
                placeholder="e.g., -8.709201"
                class="w-full border-neu-200 border rounded-3xl px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-neu-900 text-[16px] font-medium mb-[12px]">Longitude</label>
              <input
                type="text"
                placeholder="e.g., 115.168263"
                class="w-full border-neu-200 border rounded-3xl px-3 py-2"
              />
            </div>
          </div>

          <div class="items-center mt-4">
            <h1 class="text-neu-900 text-[18px] font-semibold mb-[4px]">
              Do you own, work at, or officially represent this place?
            </h1>
            <input id="representative" type="checkbox" class="mr-2" />
            <label for="representative" class="text-sm"
              >Yes! I am a representative of this place.</label
            >
          </div>

          <!-- Upload -->
          <div>
            <label class="block text-neu-900 text-[20px] font-semibold mb-[4px]">Add photos</label>
            <p class="text-neu-600 mb-[6px]">Optional</p>
            <div
              class="border-2 border-pr-500 border-dashed rounded px-4 py-[72px] text-center text-sm bg-neu-100 text-neu-600"
            >
              <div class="flex justify-center items-center">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  class=""
                >
                  <mask
                    id="mask0_524_3113"
                    style="mask-type: luminance"
                    maskUnits="userSpaceOnUse"
                    x="2"
                    y="2"
                    width="20"
                    height="20"
                  >
                    <path
                      fill-rule="evenodd"
                      clip-rule="evenodd"
                      d="M2 2H21.953V21.9539H2V2Z"
                      fill="white"
                    />
                  </mask>
                  <g mask="url(#mask0_524_3113)">
                    <path
                      fill-rule="evenodd"
                      clip-rule="evenodd"
                      d="M7.651 3.5C5.13 3.5 3.5 5.229 3.5 7.904V16.05C3.5 18.726 5.13 20.454 7.651 20.454H16.297C18.822 20.454 20.453 18.726 20.453 16.05V7.904C20.455 6.541 20.039 5.403 19.251 4.614C18.523 3.885 17.504 3.5 16.302 3.5H7.651ZM16.297 21.954H7.651C4.271 21.954 2 19.581 2 16.05V7.904C2 4.373 4.271 2 7.651 2H16.302C17.91 2 19.297 2.537 20.312 3.554C21.373 4.616 21.955 6.161 21.953 7.905V16.05C21.953 19.581 19.68 21.954 16.297 21.954Z"
                      fill="#40916C"
                    />
                  </g>
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M8.85672 7.68945C8.25272 7.68945 7.76172 8.18045 7.76172 8.78545C7.76172 9.38945 8.25272 9.88045 8.85772 9.88045C9.46172 9.88045 9.95372 9.38945 9.95372 8.78645C9.95272 8.18145 9.46072 7.69045 8.85672 7.68945ZM8.85772 11.3805C7.42572 11.3805 6.26172 10.2165 6.26172 8.78545C6.26172 7.35345 7.42572 6.18945 8.85772 6.18945C10.2887 6.19045 11.4527 7.35445 11.4537 8.78445V8.78545C11.4537 10.2165 10.2897 11.3805 8.85772 11.3805Z"
                    fill="#40916C"
                  />
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M3.74893 20.111C3.62493 20.111 3.49893 20.08 3.38293 20.015C3.02093 19.812 2.89393 19.355 3.09593 18.994C3.15593 18.886 4.59093 16.349 6.16993 15.049C7.42193 14.019 8.76993 14.585 9.85593 15.042C10.4949 15.311 11.0989 15.565 11.6789 15.565C12.2109 15.565 12.8779 14.625 13.4679 13.796C14.2869 12.64 15.2169 11.332 16.5789 11.332C18.7489 11.332 20.6219 13.268 21.6289 14.308L21.7449 14.428C22.0329 14.725 22.0259 15.2 21.7289 15.489C21.4339 15.778 20.9589 15.771 20.6689 15.473L20.5509 15.351C19.6989 14.47 18.1129 12.832 16.5789 12.832C15.9909 12.832 15.3009 13.805 14.6899 14.664C13.8519 15.844 12.9849 17.065 11.6789 17.065C10.7959 17.065 9.98693 16.725 9.27393 16.424C8.13993 15.946 7.62593 15.793 7.12293 16.207C5.75893 17.331 4.41693 19.705 4.40393 19.728C4.26693 19.973 4.01193 20.111 3.74893 20.111Z"
                    fill="#40916C"
                  />
                </svg>
              </div>
              <p class="text-[14px]">
                <span class="text-pr-500 text-[14px] font-medium">Click to add photos </span><br />
                or drag & drop
              </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup lang="ts">
import Exit from '@/components/icons/Exit.vue';
import Photo from '@/components/icons/Photo.vue';

</script>

<template>
    <div class="flex overflow-hidden font-pr text-neu-900 relative">
      <!-- Sidebar -->
      <div
        class="min-w-64 flex flex-col gap-10 p-4 min-h-screen bg-sur-50 border-r border-neu-200"
      >
        <h1 class="text-2xl font-se font-semibold pl-3">
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div class="space-y-4 text-sm">
          <div class="space-y-3">
            <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">
              Master
            </h3>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex gap-3 items-center text-pr-500 py-2 px-4 font-medium bg-[#EFF6F2] hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <svg
                class="text-pr-500 size-5"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <mask
                  id="mask0_344_1195"
                  style="mask-type: luminance"
                  maskUnits="userSpaceOnUse"
                  x="1"
                  y="0"
                  width="18"
                  height="19"
                >
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M1.66663 0.833496H18.7498V18.7543H1.66663V0.833496Z"
                    fill="white"
                  />
                </mask>
                <g mask="url(#mask0_344_1195)">
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M11.4307 12.7427C12.434 12.7427 13.2507 13.5536 13.2507 14.5502V17.1136C13.2507 17.3277 13.4223 17.4994 13.6423 17.5044H15.2307C16.4823 17.5044 17.4998 16.4994 17.4998 15.2644V7.99442C17.494 7.56942 17.2915 7.16942 16.944 6.90358L11.4498 2.52192C10.7123 1.93775 9.68067 1.93775 8.94067 2.52358L3.484 6.90192C3.12317 7.17608 2.92067 7.57608 2.9165 8.00858V15.2644C2.9165 16.4994 3.934 17.5044 5.18567 17.5044H6.789C7.01484 17.5044 7.19817 17.3252 7.19817 17.1052C7.19817 17.0569 7.204 17.0086 7.214 16.9627V14.5502C7.214 13.5594 8.02567 12.7494 9.0215 12.7427H11.4307ZM15.2307 18.7544H13.6273C12.709 18.7327 12.0007 18.0119 12.0007 17.1136V14.5503C12.0007 14.2428 11.7448 13.9928 11.4307 13.9928H9.02567C8.71817 13.9944 8.464 14.2453 8.464 14.5503V17.1053C8.464 17.1678 8.45567 17.2278 8.43817 17.2844C8.34817 18.1094 7.64317 18.7544 6.789 18.7544H5.18567C3.24484 18.7544 1.6665 17.1886 1.6665 15.2644V8.00275C1.67484 7.17442 2.0565 6.41608 2.71567 5.91692L8.1615 1.54608C9.36067 0.596083 11.0315 0.596082 12.2282 1.54442L17.7132 5.91942C18.3573 6.41025 18.739 7.16692 18.7498 7.98525V15.2644C18.7498 17.1886 17.1715 18.7544 15.2307 18.7544Z"
                    fill="currentColor"
                  />
                </g>
              </svg>
              Dashboard
            </div>
          </div>
          <div class="space-y-3">
            <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">
              User
            </h3>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <svg
                class="text-neu-500 size-5"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M9.88308 10.9484H9.90558C12.0056 10.9484 13.7131 9.24004 13.7131 7.14087C13.7131 5.04171 12.0056 3.33337 9.90558 3.33337C7.80641 3.33337 6.09891 5.04171 6.09891 7.13837C6.09474 8.15254 6.48558 9.10754 7.20058 9.82671C7.91391 10.5467 8.86641 10.945 9.88308 10.9484ZM7.34891 7.14087C7.34891 5.73087 8.49558 4.58337 9.90558 4.58337C11.3156 4.58337 12.4631 5.73087 12.4631 7.14087C12.4631 8.55171 11.3156 9.69837 9.90558 9.69837H9.88474C9.20474 9.69587 8.56641 9.42837 8.08724 8.94587C7.60808 8.46337 7.34641 7.82421 7.34891 7.14087Z"
                  fill="currentColor"
                />
                <path
                  d="M14.2873 9.5838C14.3315 9.8963 14.599 10.1221 14.9056 10.1221C14.934 10.1221 14.9631 10.1205 14.9923 10.1163C16.4715 9.9088 17.589 8.62546 17.5923 7.12963C17.5923 5.6438 16.5281 4.39046 15.0631 4.14963C14.7206 4.09546 14.4015 4.3238 14.3448 4.66463C14.289 5.00546 14.5198 5.32713 14.8598 5.38296C15.719 5.5238 16.3423 6.2588 16.3423 7.12796C16.3406 8.00463 15.6865 8.7563 14.8198 8.87796C14.4773 8.92546 14.2398 9.2413 14.2873 9.5838Z"
                  fill="currentColor"
                />
                <path
                  d="M16.8003 15.0402C16.8953 15.2893 17.1328 15.4427 17.3845 15.4427C17.4586 15.4427 17.5336 15.4293 17.607 15.4018C18.7986 14.9477 18.977 14.1202 18.977 13.6668C18.977 12.9243 18.5528 11.976 16.5336 11.6735C16.1895 11.6293 15.8728 11.8568 15.822 12.1985C15.7711 12.541 16.007 12.8585 16.3478 12.9102C17.2628 13.0468 17.727 13.3018 17.727 13.6668C17.727 13.781 17.727 14.0185 17.162 14.2335C16.8395 14.356 16.677 14.7177 16.8003 15.0402Z"
                  fill="currentColor"
                />
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M9.90555 17.3258C8.52305 17.3258 4.31472 17.3258 4.31472 14.6633C4.31472 12.0117 8.52305 12.0117 9.90555 12.0117C11.2881 12.0117 15.4956 12.0117 15.4956 14.6775C15.4956 17.3258 11.4347 17.3258 9.90555 17.3258ZM9.90555 13.2617C7.92555 13.2617 5.56472 13.505 5.56472 14.6633C5.56472 15.8308 7.92555 16.0758 9.90555 16.0758C11.8856 16.0758 14.2456 15.8333 14.2456 14.6775C14.2456 13.5075 11.8856 13.2617 9.90555 13.2617Z"
                  fill="currentColor"
                />
                <path
                  d="M4.90471 10.1221C4.87637 10.1221 4.84721 10.1204 4.81804 10.1162C3.33887 9.90875 2.22221 8.62542 2.21887 7.13125C2.21887 5.64375 3.28304 4.39042 4.74804 4.14958C5.09887 4.09458 5.40971 4.32542 5.46637 4.66458C5.52221 5.00542 5.29137 5.32708 4.95137 5.38292C4.09221 5.52375 3.46887 6.25875 3.46887 7.12958C3.47054 8.00458 4.12471 8.75708 4.99054 8.87792C5.33304 8.92542 5.57054 9.24125 5.52304 9.58375C5.47887 9.89625 5.21137 10.1221 4.90471 10.1221Z"
                  fill="currentColor"
                />
                <path
                  d="M2.20421 15.4019C2.27754 15.4294 2.35254 15.4427 2.42671 15.4427C2.67837 15.4427 2.91587 15.2894 3.01087 15.0402C3.13421 14.7177 2.97171 14.356 2.64921 14.2335C2.08337 14.0177 2.08337 13.781 2.08337 13.6669C2.08337 13.3019 2.54754 13.0469 3.46254 12.9102C3.80337 12.8585 4.03921 12.541 3.98837 12.1985C3.93671 11.8569 3.62171 11.6302 3.27754 11.6735C1.25754 11.976 0.833374 12.9252 0.833374 13.6669C0.833374 14.1194 1.01171 14.9469 2.20421 15.4019Z"
                  fill="currentColor"
                />
              </svg>
              Management
            </div>
          </div>
          <div class="space-y-3">
            <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">
              Katalog
            </h3>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <svg
                class="text-neu-500 size-5"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M12.3092 8.33342C11.2205 8.33342 10.3349 9.21906 10.3349 10.3089C10.3349 11.3976 11.2205 12.2821 12.3092 12.2821C13.398 12.2821 14.2836 11.3976 14.2836 10.3089C14.2836 9.21906 13.398 8.33342 12.3092 8.33342M12.3092 13.9744C10.2875 13.9744 8.64258 12.3307 8.64258 10.3089C8.64258 8.28604 10.2875 6.64111 12.3092 6.64111C14.331 6.64111 15.9759 8.28604 15.9759 10.3089C15.9759 12.3307 14.331 13.9744 12.3092 13.9744"
                  fill="currentColor"
                />
                <mask
                  id="mask0_693_2067"
                  style="mask-type: luminance"
                  maskUnits="userSpaceOnUse"
                  x="3"
                  y="1"
                  width="19"
                  height="22"
                >
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M3 1H21.6148V23H3V1Z"
                    fill="white"
                  />
                </mask>
                <g mask="url(#mask0_693_2067)">
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M12.3065 2.69231C8.10737 2.69231 4.69116 6.14123 4.69116 10.3788C4.69116 15.7705 11.0362 21.0234 12.3065 21.3032C13.5769 21.0223 19.9219 15.7693 19.9219 10.3788C19.9219 6.14123 16.5057 2.69231 12.3065 2.69231V2.69231ZM12.3067 23C10.2827 23 2.99902 16.7362 2.99902 10.3788C2.99902 5.20708 7.17451 1 12.3067 1C17.4389 1 21.6144 5.20708 21.6144 10.3788C21.6144 16.7362 14.3307 23 12.3067 23V23Z"
                    fill="currentColor"
                  />
                </g>
              </svg>
              Destinations
            </div>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <svg
                class="text-neu-500 size-5"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7.97333 2.5H4.375C3.87772 2.5 3.40081 2.69754 3.04917 3.04917C2.69754 3.40081 2.5 3.87772 2.5 4.375V7.97333C2.5 8.47083 2.6975 8.94833 3.04917 9.29917L11.0333 17.2833C11.6158 17.8658 12.5167 18.01 13.2058 17.5583C14.9405 16.4222 16.4222 14.9405 17.5583 13.2058C18.01 12.5167 17.8658 11.6158 17.2833 11.0333L9.3 3.05C9.12586 2.87564 8.91905 2.73732 8.69141 2.64295C8.46377 2.54857 8.21976 2.5 7.97333 2.5Z"
                  stroke="currentColor"
                  stroke-width="1.4"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M5 5H5.00667V5.00667H5V5Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              Categories
            </div>
          </div>
          <div class="space-y-3">
            <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">
              REVIEWS
            </h3>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <svg
                class="text-neu-500 size-5"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M11.2015 17.7437L11.6427 16.9983L10.592 16.3763L10.1507 17.1218L11.2015 17.7437ZM7.94052 16.9983L8.38178 17.7437L9.43243 17.1218L8.99118 16.3763L7.94052 16.9983ZM10.1507 17.1218C9.99389 17.3869 9.58936 17.3869 9.43243 17.1218L8.38178 17.7437C9.01145 18.8075 10.5718 18.8075 11.2015 17.7437L10.1507 17.1218ZM8.5707 2.26256H11.0126V1.04163H8.5707V2.26256ZM17.3207 8.5707V9.38465H18.5416V8.5707H17.3207ZM2.26256 9.38465V8.5707H1.04163V9.38465H2.26256ZM1.04163 9.38465C1.04163 10.3244 1.04129 11.0598 1.08176 11.653C1.12261 12.2516 1.20705 12.7499 1.39789 13.2106L2.52588 12.7433C2.40693 12.4562 2.33647 12.1063 2.29987 11.5699C2.26289 11.0279 2.26256 10.3411 2.26256 9.38465H1.04163ZM6.37506 14.872C5.35319 14.8543 4.81774 14.7894 4.39804 14.6155L3.93081 15.7435C4.58602 16.0149 5.33228 16.0751 6.35402 16.0927L6.37506 14.872ZM1.39789 13.2106C1.8729 14.3573 2.78402 15.2685 3.93081 15.7435L4.39804 14.6155C3.55041 14.2644 2.87698 13.591 2.52588 12.7433L1.39789 13.2106ZM17.3207 9.38465C17.3207 10.3411 17.3204 11.0279 17.2834 11.5699C17.2468 12.1063 17.1763 12.4562 17.0574 12.7433L18.1854 13.2106C18.3762 12.7499 18.4606 12.2516 18.5015 11.653C18.542 11.0598 18.5416 10.3244 18.5416 9.38465H17.3207ZM13.2292 16.0927C14.251 16.0751 14.9973 16.0149 15.6524 15.7435L15.1852 14.6155C14.7655 14.7894 14.23 14.8543 13.2082 14.872L13.2292 16.0927ZM17.0574 12.7433C16.7062 13.591 16.0329 14.2644 15.1852 14.6155L15.6524 15.7435C16.7992 15.2685 17.7103 14.3573 18.1854 13.2106L17.0574 12.7433ZM11.0126 2.26256C12.3566 2.26256 13.3217 2.2632 14.0746 2.33478C14.8184 2.4055 15.2916 2.54112 15.6689 2.77232L16.3068 1.73131C15.7054 1.36279 15.0232 1.19855 14.1901 1.11933C13.3661 1.04098 12.333 1.04163 11.0126 1.04163V2.26256ZM18.5416 8.5707C18.5416 7.25031 18.5423 6.21715 18.4639 5.39311C18.3847 4.55999 18.2204 3.87781 17.852 3.27644L16.8109 3.91438C17.0422 4.29167 17.1778 4.76493 17.2485 5.50868C17.32 6.26151 17.3207 7.22666 17.3207 8.5707H18.5416ZM15.6689 2.77232C16.1344 3.05756 16.5257 3.44891 16.8109 3.91438L17.852 3.27644C17.4661 2.64669 16.9366 2.11722 16.3068 1.73131L15.6689 2.77232ZM8.5707 1.04163C7.25031 1.04163 6.21715 1.04098 5.39311 1.11933C4.55999 1.19855 3.87781 1.36279 3.27644 1.73131L3.91438 2.77232C4.29167 2.54112 4.76493 2.4055 5.50868 2.33478C6.26151 2.2632 7.22666 2.26256 8.5707 2.26256V1.04163ZM2.26256 8.5707C2.26256 7.22666 2.2632 6.26151 2.33478 5.50868C2.40549 4.76493 2.54112 4.29167 2.77232 3.91438L1.73131 3.27644C1.36279 3.87781 1.19855 4.55999 1.11933 5.39311C1.04098 6.21715 1.04163 7.25031 1.04163 8.5707H2.26256ZM3.27644 1.73131C2.64669 2.11722 2.11722 2.64669 1.73131 3.27644L2.77232 3.91438C3.05756 3.44891 3.44891 3.05756 3.91438 2.77232L3.27644 1.73131ZM8.99118 16.3763C8.82595 16.0972 8.6809 15.8508 8.53985 15.6572C8.39122 15.4534 8.22086 15.2699 7.98453 15.1324L7.3707 16.1878C7.40929 16.2102 7.46186 16.2512 7.55313 16.3763C7.65192 16.512 7.76354 16.6992 7.94052 16.9983L8.99118 16.3763ZM6.35402 16.0927C6.71142 16.0989 6.9378 16.1034 7.11037 16.1225C7.27162 16.1404 7.33412 16.1665 7.3707 16.1878L7.98453 15.1324C7.74624 14.9938 7.49828 14.937 7.24474 14.909C7.00252 14.8822 6.70979 14.8778 6.37506 14.872L6.35402 16.0927ZM11.6427 16.9983C11.8197 16.6992 11.9313 16.512 12.0301 16.3763C12.1213 16.2512 12.1739 16.2102 12.2125 16.1878L11.5987 15.1324C11.3624 15.2699 11.192 15.4534 11.0434 15.6572C10.9023 15.8508 10.7573 16.0972 10.592 16.3763L11.6427 16.9983ZM13.2082 14.872C12.8734 14.8778 12.5807 14.8822 12.3385 14.909C12.0849 14.937 11.837 14.9938 11.5987 15.1324L12.2125 16.1878C12.2491 16.1665 12.3116 16.1404 12.4729 16.1225C12.6454 16.1034 12.8718 16.0989 13.2292 16.0927L13.2082 14.872Z"
                  fill="currentColor"
                />
              </svg>
              Testimonials
            </div>
            <div
              :to="{ name: 'Wishlist' }"
              class="flex justify-between items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
            >
              <span class="flex items-center gap-3"
                ><svg
                  class="text-neu-500 size-5"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M9.16663 13.3333C9.16663 13.7935 9.53971 14.1666 9.99996 14.1666C10.4602 14.1666 10.8333 13.7935 10.8333 13.3333H9.16663ZM6.84635 11.9935C7.29576 11.8942 7.57961 11.4495 7.48035 11C7.38108 10.5506 6.93631 10.2668 6.4869 10.366L6.84635 11.9935ZM13.513 10.366C13.0636 10.2668 12.6188 10.5506 12.5195 11C12.4203 11.4495 12.7041 11.8942 13.1535 11.9935L13.513 10.366ZM12.5 5.83329C12.5 7.214 11.3807 8.33329 9.99996 8.33329V9.99996C12.3011 9.99996 14.1666 8.13448 14.1666 5.83329H12.5ZM9.99996 8.33329C8.61921 8.33329 7.49996 7.214 7.49996 5.83329H5.83329C5.83329 8.13448 7.69878 9.99996 9.99996 9.99996V8.33329ZM7.49996 5.83329C7.49996 4.45258 8.61921 3.33329 9.99996 3.33329V1.66663C7.69878 1.66663 5.83329 3.53211 5.83329 5.83329H7.49996ZM9.99996 3.33329C11.3807 3.33329 12.5 4.45258 12.5 5.83329H14.1666C14.1666 3.53211 12.3011 1.66663 9.99996 1.66663V3.33329ZM9.16663 9.16663V13.3333H10.8333V9.16663H9.16663ZM16.6666 14.1666C16.6666 14.3557 16.5839 14.5985 16.3069 14.8896C16.0259 15.185 15.5798 15.4888 14.9648 15.7621C13.737 16.3078 11.9824 16.6666 9.99996 16.6666V18.3333C12.1597 18.3333 14.155 17.9459 15.6417 17.2851C16.384 16.9552 17.0362 16.5409 17.5142 16.0385C17.9963 15.532 18.3333 14.898 18.3333 14.1666H16.6666ZM9.99996 16.6666C8.01758 16.6666 6.26294 16.3078 5.03511 15.7621C4.42014 15.4888 3.97406 15.185 3.69301 14.8896C3.41604 14.5985 3.33329 14.3557 3.33329 14.1666H1.66663C1.66663 14.898 2.00361 15.532 2.48568 16.0385C2.96367 16.5409 3.61594 16.9552 4.35821 17.2851C5.84484 17.9459 7.8402 18.3333 9.99996 18.3333V16.6666ZM3.33329 14.1666C3.33329 13.902 3.50667 13.5111 4.13626 13.0688C4.75103 12.637 5.67949 12.2512 6.84635 11.9935L6.4869 10.366C5.18423 10.6538 4.02936 11.107 3.17818 11.705C2.34182 12.2926 1.66663 13.1225 1.66663 14.1666H3.33329ZM13.1535 11.9935C14.3205 12.2512 15.2489 12.637 15.8636 13.0688C16.4933 13.5111 16.6666 13.902 16.6666 14.1666H18.3333C18.3333 13.1225 17.6581 12.2926 16.8217 11.705C15.9705 11.107 14.8157 10.6538 13.513 10.366L13.1535 11.9935Z"
                    fill="currentColor"
                  />
                </svg>
                Suggested Spot</span
              ><span
                class="flex items-center text-neu-50 text-sm rounded-[6px] justify-center px-2 bg-pr-500"
                >2</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Left COnten -->
      <div class="flex-1 flex flex-col">
        <div
          class="flex justify-end items-center px-6 py-3.5 bg-sur-50 border-b border-neu-200"
        >
          <div class="gap-3 w-fit flex items-center">
            <img
              src="@/assets/images/User Avatar.jpg"
              alt="User Profile"
              class="size-9 rounded-full"
            />
            <p
              class="text-neu-900 gap-0.5 flex items-center font-medium text-sm max-w-36 line-clamp-1"
            >
              Udin Surudin
              <svg
                class="text-neu-900"
                width="18"
                height="18"
                viewBox="0 0 18 18"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M3.35225 5.97725C3.55195 5.77755 3.86445 5.7594 4.08466 5.92279L4.14775 5.97725L9 10.8293L13.8523 5.97725C14.052 5.77755 14.3645 5.7594 14.5847 5.92279L14.6477 5.97725C14.8474 6.17695 14.8656 6.48945 14.7022 6.70966L14.6477 6.77275L9.39775 12.0227C9.19805 12.2224 8.88555 12.2406 8.66534 12.0772L8.60225 12.0227L3.35225 6.77275C3.13258 6.55308 3.13258 6.19692 3.35225 5.97725Z"
                  fill="currentColor"
                />
              </svg>
            </p>
          </div>
        </div>
        <div class="flex-1">
          <!-- Kalian tambahkan kodenya disini ya -->
          <div class="px-6 sm:px-16 lg:px-[32px] pb-24 md:pb-30">
            <div class="mt-[24px]">
              <h1
                class="text-4xl sm:text-[32px] font-semibold leading-12 sm:leading-[62px] font-se"
              >
                Create Destination
              </h1>
              <p>
                Katalog
                <span class="text-neu-500">> Destinations > Create</span>
              </p>
            </div>

            <form
              class="flex flex-col lg:flex-row gap-6 lg:gap-[32px] mt-10 md:mt-6"
            >
              <!-- Form Left -->
              <div
                class="py-4 px-4 w-full lg:w-2/3 border border-neu-200 rounded-3xl"
              >
                <div
                  class="w-full lg:w-full lg:min-w-full xl:min-w-120 flex flex-col gap-6"
                >
                  <div class="flex flex-col gap-3">
                    <label for="name" class="text-base md:text-lg font-semibold"
                      >Name</label
                    >
                    <input
                      type="text"
                      id="name"
                      placeholder="e.g., Hidden Gem Beach Club"
                      class="px-4 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                    />
                  </div>
                  <div class="flex flex-col gap-3">
                    <label
                      for="category"
                      class="text-base md:text-lg font-semibold"
                      >Category</label
                    >
                    <div class="relative w-full">
                      <select
                        id="category"
                        class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none"
                      >
                        <option value="" disabled selected hidden>
                          Select a category — Beach, Temple, Mountain, etc.
                        </option>
                        <option value="beach">Beach</option>
                        <option value="temple">Temple</option>
                        <option value="mountain">Mountain</option>
                      </select>
                      <ArrowDown
                        class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
                      />
                    </div>
                  </div>
                  <div class="flex flex-col gap-3">
                    <label
                      for="descriptions"
                      class="text-base md:text-lg font-semibold"
                      >Descriptions</label
                    >
                    <textarea
                      id="descriptions"
                      rows="7"
                      placeholder="Tell us what makes this place special..."
                      class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
                    ></textarea>
                  </div>

                  <div class="flex flex-col gap-3">
                    <label
                      for="category"
                      class="text-base md:text-lg font-semibold"
                      >Facilities</label
                    >
                    <ul
                      class="flex flex-wrap text-sm sm:text-base gap-3 sm:gap-4"
                    >
                      <li
                        class="bg-[#F2F8F5] text-pr-500 gap-1 font-medium items-center px-4 py-2 rounded-full flex"
                      >
                        Parking Area<Exit class="size-4" />
                      </li>
                      <li
                        class="bg-[#F2F8F5] text-pr-500 gap-1 font-medium items-center px-4 py-2 rounded-full flex"
                      >
                        Restrooms<Exit class="size-4" />
                      </li>
                    </ul>
                    <div class="relative w-full">
                      <select
                        id="category"
                        class="w-full px-3 py-3 text-sm text-neu-900 border border-neu-200 rounded-full appearance-none"
                      >
                        <option value="" disabled selected hidden>
                          Select a facility option
                        </option>
                        <option value="parking-area">Parking Area</option>
                        <option value="restrooms">Restrooms</option>
                      </select>
                      <ArrowDown
                        class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400"
                      />
                    </div>
                  </div>
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Entrance Ticket</label
                    >
                    <div class="flex gap-2.5 items-center w-full">
                      <div class="flex-1">
                        <input
                          type="text"
                          placeholder="Rp 75.000"
                          class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
                        />
                      </div>

                      <div class="flex-shrink-0">
                        <Subtract class="w-4 h-4 text-neu-900" /> -
                      </div>

                      <div class="flex-1">
                        <input
                          type="text"
                          placeholder="Rp 120.000"
                          class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
                        />
                      </div>
                    </div>
                  </div>

                  <div class="flex flex-col gap-3">
                    <h3 class="text-base md:text-lg font-semibold">Contact</h3>
                    <label class="font-semibold">Phone Number</label>
                    <input
                      type="text"
                      placeholder="e.g., +62 812 3456 7890"
                      class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                    />
                    <label class="font-semibold mt-1">Mail</label>
                    <input
                      type="text"
                      placeholder="e.g., info@spot.com"
                      class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                    />
                  </div>

                  <div class="flex flex-col gap-3">
                    <label for="name" class="text-base md:text-lg font-semibold"
                      >Photo</label
                    >
                    <div class="w-full">
                      <label
                        for="photo-upload"
                        class="flex flex-col items-center justify-center w-full h-40 border-[1.6px] border-dashed border-pr-500 rounded-3xl cursor-pointer bg-gray-100 hover:bg-gray-200 transition"
                      >
                        <Photo class="mb-1" />

                        <!-- Text -->
                        <p class="text-pr-500 font-medium text-sm mb-[2px]">
                          Click to add photos
                        </p>
                        <p class="text-neu-900 text-sm">or drag & drop</p>

                        <!-- Hidden input -->
                        <input
                          id="photo-upload"
                          type="file"
                          class="hidden"
                          multiple
                        />
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Form Right -->
              <div
                class="py-6 px-6 w-full lg:w-1/3 border border-neu-200 rounded-3xl"
              >
                <div class="flex flex-col gap-6">
                  <!-- Map -->
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Map Location</label
                    >
                    <div
                      class="w-full h-80 xl:h-[400px] rounded-3xl overflow-hidden"
                    >
                      <iframe
                        class="w-full h-full"
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade"
                      ></iframe>
                    </div>
                  </div>

                  <!-- Street -->
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Street</label
                    >
                    <input
                      type="text"
                      placeholder="e.g., Jalan Pantai Kuta"
                      class="px-3 py-3 text-sm border border-gray-300 rounded-full"
                    />
                  </div>

                  <!-- Sub-district -->
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Sub-district</label
                    >
                    <input
                      type="text"
                      placeholder="e.g., Kuta"
                      class="px-3 py-3 text-sm border border-gray-300 rounded-full"
                    />
                  </div>

                  <!-- Regency -->
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Regency</label
                    >
                    <input
                      type="text"
                      placeholder="e.g., Badung"
                      class="px-3 py-3 text-sm border border-gray-300 rounded-full"
                    />
                  </div>

                  <!-- Latitude & Longitude -->
                  <div class="flex flex-col gap-3">
                    <label class="text-base md:text-lg font-semibold"
                      >Coordinates</label
                    >
                    <div class="flex gap-6">
                      <div class="flex flex-col gap-2 w-1/2">
                        <label class="text-sm font-medium">Latitude</label>
                        <input
                          type="text"
                          placeholder="e.g., -8.709201"
                          class="px-3 py-3 text-sm border border-gray-300 rounded-full"
                        />
                      </div>
                      <div class="flex flex-col gap-2 w-1/2">
                        <label class="text-sm font-medium">Longitude</label>
                        <input
                          type="text"
                          placeholder="e.g., 115.168263"
                          class="px-3 py-3 text-sm border border-gray-300 rounded-full"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
            <div class="space-x-[10px] mt-[24px]">
              <button
                type="submit"
                class="bg-pr-500 text-neu-50 px-6 text-base sm:text-lg py-2 font-medium rounded-full"
              >
                Create
              </button>

              <button
                type="button"
                class="text-neu-900 border border-neu-900 px-6 text-base sm:text-lg py-2 font-medium rounded-full"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
        <div
          class="flex w-full h-fit items-center px-6 py-4 bg-sur-50 border-t border-neu-200"
        >
          <p class="text-neu-500">
            © 2024, Made with ❤️ by <span class="text-pr-500">Balinara</span>
          </p>
        </div>
      </div>
    </div>
</template>
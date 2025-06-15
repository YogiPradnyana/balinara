<script setup>
import { RouterView } from 'vue-router'
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
</script>

<template>
  <div class="antialiased">
    <Toaster position="top-right" :expand="true" />
    <RouterView :key="$route.fullPath" />
  </div>
</template>

<style>
/* ... style global Anda yang lain ... */

/* === KUSTOMISASI VUE-SONNER === */

/* Menargetkan semua ikon di dalam toast sukses */
/* Atribut [data-type="success"] akan muncul jika Anda menggunakan `richColors` */
[data-sonner-toast][data-type='success'] [data-icon] {
  color: #5cce74; /* Ganti dengan warna hijau yang Anda inginkan, misal: Tailwind's Emerald 400 */
}

/* Menargetkan semua ikon di dalam toast error */
[data-sonner-toast][data-type='error'] [data-icon] {
  color: #f87171; /* Ganti dengan warna merah yang Anda inginkan, misal: Tailwind's Red 400 */
}

/* Menargetkan semua ikon di dalam toast info */
[data-sonner-toast][data-type='info'] [data-icon] {
  color: #60a5fa; /* Ganti dengan warna biru yang Anda inginkan */
}

/* Menargetkan semua ikon di dalam toast warning */
[data-sonner-toast][data-t-warning] [data-icon] {
  color: #facc15; /* Ganti dengan warna kuning yang Anda inginkan */
}
</style>

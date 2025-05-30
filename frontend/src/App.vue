<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="antialiased">
    <RouterView :key="$route.fullPath" />
  </div>
</template>
